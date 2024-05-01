import requests
import sqlite3
import sys

def read_api_key(file):
    try:
        with open('api_key_lastfm.txt', 'r') as f:
            api_key = f.readline().strip()
            return api_key
    except FileNotFoundError:
        print(f"Error: {'api_key_lastfm.txt'} not found.")
        return None

def connect_to_database(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()
    return conn, cur

def create_top_artists_table(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS top_artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Playcount INTEGER,
            Listeners INTEGER
        )
    ''')

def fetch_top_artists(API_URL, params):
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        sys.exit(1)

def insert_top_artists(cur, artists_data):
    total_items = 0
    for artist in artists_data:
        name = artist['name']
        playcount = int(artist['playcount'])
        listeners = int(artist['listeners'])

        # Check if the artist already exists in the database
        cur.execute('SELECT COUNT(*) FROM top_artists WHERE Name = ?', (name,))
        if cur.fetchone()[0] > 0:
            continue  # Skip inserting if the artist already exists

        try:
            cur.execute('''
                INSERT INTO top_artists (Name, Playcount, Listeners)
                VALUES (?, ?, ?)
            ''', (name, playcount, listeners))
            total_items += 1
        except sqlite3.IntegrityError:
            pass

    return total_items

def main():
    conn, cur = connect_to_database('complete.db')

    create_top_artists_table(cur)

    cur.execute("SELECT COUNT(*) FROM top_artists")
    existing_count = cur.fetchone()[0]

    API_KEY = read_api_key("api_key_lastfm.txt")
    API_URL = "https://ws.audioscrobbler.com/2.0/"
    method = "chart.getTopArtists"
    limit = 50
    total_items = existing_count
    page = 1

    params = {
        "method": method,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit,
        "page": page
    }

    response_data = fetch_top_artists(API_URL, params)

    if 'artists' in response_data and 'artist' in response_data['artists']:
        while total_items < (existing_count + 25):
            print(total_items)

            artists_data = response_data['artists']['artist']

            total_artists_inserted = insert_top_artists(cur, artists_data[:25])
            print(f"Inserted {total_artists_inserted} new artists into top_artists table.")

            cur.execute("SELECT COUNT(1) FROM top_artists")
            total_artists = cur.fetchone()[0]

            if total_artists >= existing_count + 25:
                break

            page += 1
            params['page'] = page
            response_data = fetch_top_artists(API_URL, params)
    else:
        print("Error: Unable to fetch top artists data.")

    conn.commit()
    conn.close()
    print("Data stored in SQLite database successfully!")

if __name__ == "__main__":
    main()

