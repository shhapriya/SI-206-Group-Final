
import json
import os
import requests
import sqlite3


API_KEY = "13021dfb347b4592b5c6f6195b4f00e1"

# def gather_player_data(cur, conn):
#     cur.execute('''CREATE TABLE IF NOT EXISTS players
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                        name TEXT,
#                        salary INTEGER,
#                        weight INTEGER,
#                        height INTEGER,
#                        experience INTEGER,
#                     depthchartorder INTEGER)''')
    
#     url = "http://archive.sportsdata.io/v3/nba/stats/json/players/2023-11-13-15-51.json"
#     headers = {"Ocp-Apim-Subscription-Key": API_KEY}
#     response = requests.get(url, headers=headers)
#     players_data = json.loads(response.content.decode('utf-8'))
    
#     cur.execute("SELECT COUNT(name) FROM players")
#     current_count = cur.fetchone()[0]
#     new_players_count = 0
#     print(f"Current number of players in database: {current_count}")
#     for player in players_data:
#         if new_players_count >= 25:
#             break
#         if player['BirthCountry'] == "USA":
#             name = player["FirstName"] + " " + player["LastName"]
#             try:
#                 salary = player.get("Salary", 0)  
#                 weight = player.get("Weight", 0)
#                 height = player.get("Height", 0)
#                 depthchartorder = player.get("DepthChartOrder", 0)
#                 experience = int(player.get("Experience", 0))
#                 cur.execute('''INSERT OR IGNORE INTO players (
#                          name, salary, weight, height, experience, depthchartorder)
#                          VALUES (?, ?, ?, ?, ?, ?)''',
#                 (name, salary, weight, height, experience, depthchartorder))
#                 if cur.rowcount > 0:
#                     new_players_count += 1
#                     print(f"Inserted player: {name}")
#             except sqlite3.IntegrityError:
#                 # This means the player already exists in the database, so we skip
#                 print(f"Skipping existing player: {name}")
#                 continue
#     conn.commit()
#     print(f"Inserted {new_players_count} new players.")

def gather_player_data(cur, conn):
    # Create players table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS players
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 salary INTEGER,
                 weight INTEGER,
                 height INTEGER,
                 experience INTEGER,
                 depthchartorder INTEGER)''')

    # Create player_ids table to keep track of inserted player IDs
    cur.execute('''CREATE TABLE IF NOT EXISTS player_ids
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 player_id INTEGER UNIQUE)''')

    url = "http://archive.sportsdata.io/v3/nba/stats/json/players/2023-11-13-15-51.json"
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    response = requests.get(url, headers=headers)
    players_data = json.loads(response.content.decode('utf-8'))

    # Get existing player IDs
    cur.execute("SELECT player_id FROM player_ids")
    existing_player_ids = set(row[0] for row in cur.fetchall())

    new_players_count = 0
    for player in players_data:
        if new_players_count >= 25:
            break
        if player['BirthCountry'] == "USA":
            name = player["FirstName"] + " " + player["LastName"]
            player_id = player.get("PlayerID")

            # Skip if player ID already exists in database
            if player_id in existing_player_ids:
                print(f"Skipping existing player: {name}")
                continue

            try:
                salary = player.get("Salary", 0)
                weight = player.get("Weight", 0)
                height = player.get("Height", 0)
                depthchartorder = player.get("DepthChartOrder", 0)
                experience = int(player.get("Experience", 0))

                # Insert player data into players table
                cur.execute('''INSERT INTO players (
                             name, salary, weight, height, experience, depthchartorder)
                             VALUES (?, ?, ?, ?, ?, ?)''',
                            (name, salary, weight, height, experience, depthchartorder))
                
                # Insert player ID into player_ids table
                cur.execute('''INSERT INTO player_ids (player_id) VALUES (?)''', (player_id,))
                conn.commit()

                if cur.rowcount > 0:
                    new_players_count += 1
                    print(f"Inserted player: {name}")
            except sqlite3.IntegrityError:
                print(f"Skipping existing player: {name}")
                continue

    print(f"Inserted {new_players_count} new players.")




def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + 'complete.db')
    cur = conn.cursor()
    gather_player_data(cur, conn)
    cur.close()


if __name__ == "__main__":
    main()


