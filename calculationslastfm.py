import sqlite3
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('complete.db')
cursor = conn.cursor()

# LAST FM CALCULATIONS 
def calculate_average_playcount_top_tracks(cur):
    cur.execute("""
        SELECT Avg(Playcount) FROM top_tracks
    """)
    average_playcount_top_tracks = cur.fetchone()[0]
    return average_playcount_top_tracks

def calculate_average_playcount_top_artist(cur):
    cur.execute("""
        SELECT Avg(Playcount) FROM top_artists
    """)
    average_playcount_top_artist = cur.fetchone()[0]
    return average_playcount_top_artist

def calculate_average_playcount_and_listeners_top_artists(cur):
    average_playcount_top_tracks = calculate_average_playcount_top_tracks(cur)
    average_playcount_top_artist = calculate_average_playcount_top_artist(cur)


    cur.execute("""
        SELECT top_artists.name, AVG(top_tracks.Playcount) AS average_playcount, AVG(top_tracks.Listeners) AS average_listeners
        FROM top_artists
        JOIN top_tracks ON top_artists.id = top_tracks.artistID
        GROUP BY top_artists.name
        ORDER BY average_playcount DESC
        LIMIT 10
    """)
    top_artists_data = cur.fetchall()
    
    return top_artists_data


def calculate_percentage_playcount_taylor(cur):
    cur.execute("""
        SELECT Name, Playcount FROM top_tracks
        WHERE artistID = (
            SELECT id FROM top_artists
            WHERE name = 'Taylor Swift'
        )
        ORDER BY Playcount DESC
        LIMIT 10
    """)
    taylor_top_songs_data = cur.fetchall()
    
    total_playcount = sum(row[1] for row in taylor_top_songs_data)
    percentage_playcount = [(row[0], row[1] / total_playcount * 100) for row in taylor_top_songs_data]
    
    return percentage_playcount


def write_calculated_data(average_playcount_top_tracks, average_playcount_top_artist, taylor_breakdown, top_artists_data):

    with open('calculated_data.txt', 'w') as f:
        f.write("Average Playcount for Top Tracks: {:.2f}\n".format(average_playcount_top_tracks))
        f.write("Average Playcount for Top Artists: {:.2f}\n".format(average_playcount_top_artist))
        
        if taylor_breakdown:
            f.write("\nTaylor Swift's Top Tracks Playcount Breakdown:\n")
            for track, percentage in taylor_breakdown:
                f.write(f"{track}: {percentage:.2f}%\n")
        else:
            f.write("\nNo data available for Taylor Swift's top tracks.\n")
        
        if top_artists_data:
            f.write("\nAverage Playcount vs Average Listeners for Top 10 Artists:\n")
            for data in top_artists_data:
                artist = data[0]
                avg_playcount = data[1]
                avg_listeners = data[2]
                f.write(f"{artist}: Average Playcount - {avg_playcount:.2f}, Average Listeners - {avg_listeners:.2f}\n")
        else:
            f.write("\nNo data available for the top 10 artists.\n")





# LAST FM VISUALIZATIONS

def plot_taylor_top_tracks_playcounts(percentage_playcount):
    if not percentage_playcount:
        print("No data available for Taylor Swift's top tracks.")
        return
    
    track_names = [row[0] for row in percentage_playcount]
    playcounts = [row[1] for row in percentage_playcount]
    
    plt.figure(figsize=(10, 6))
    plt.pie(playcounts, labels=track_names, autopct='%1.1f%%')
    plt.title("Taylor Swift's Top Tracks Playcount Breakdown", pad=20)  
    plt.axis('equal')
    plt.show()

def plot_average_playcount_vs_listeners(top_artists_data):
    artists = [row[0] for row in top_artists_data]
    average_playcounts = [row[1] * 100 for row in top_artists_data]  
    average_listeners = [row[2] * 100 for row in top_artists_data] 

    x = np.arange(len(artists))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, average_playcounts, width, label='Average Playcount')
    rects2 = ax.bar(x + width/2, average_listeners, width, label='Average Listeners')

    ax.set_xlabel('Artists')
    ax.set_ylabel('Average (in %)')
    ax.set_title('Average Playcount vs Average Listeners for Top 10 Artists')
    ax.set_xticks(x)
    ax.set_xticklabels(artists, rotation=45, ha='right')
    ax.legend()

    fig.tight_layout()
    plt.show()

def main(): 
    conn = sqlite3.connect('complete.db')
    cursor = conn.cursor()
    average_playcount_top_tracks = calculate_average_playcount_top_tracks(cursor)
    average_playcount_top_artist = calculate_average_playcount_top_artist(cursor)
    taylor_breakdown = calculate_percentage_playcount_taylor(cursor)
    top_artists_data = calculate_average_playcount_and_listeners_top_artists(cursor)
    print(top_artists_data)
    write_calculated_data(average_playcount_top_tracks, average_playcount_top_artist, taylor_breakdown, top_artists_data)
    plot_taylor_top_tracks_playcounts (taylor_breakdown)
    plot_average_playcount_vs_listeners(top_artists_data)

    conn.close()

if __name__ == "__main__":
     main()
