import sqlite3
import matplotlib.pyplot as plt
import numpy as np


conn = sqlite3.connect('complete.db')
cursor = conn.cursor()


def calculate_average_rating_imdb(cur):
  cur.execute("""
      SELECT AVG(COALESCE(imdb, 0)) FROM Movie_Ratings
              """)
  average_imdb_ratings = cur.fetchone()[0]
  return average_imdb_ratings




def calculate_average_rating_rotten_tomatoes(cur):
  cur.execute("""
      SELECT AVG(COALESCE(rotten_tomatoes, 0)) FROM Movie_Ratings
              """)
  average_rotten_tom_ratings = cur.fetchone()[0]
  return average_rotten_tom_ratings




def calculate_average_rating_metacritic(cur):
  cur.execute("""
      SELECT AVG(COALESCE(metacritic, 0)) FROM Movie_Ratings
  """)
  average_metacritic_ratings = cur.fetchone()[0]
  return average_metacritic_ratings




def calculate_percentage_rating_above_two_imdb(cur):
  cur.execute("""
      SELECT imdb FROM Movie_Ratings WHERE imdb > 2.0 AND imdb IS NOT NULL
  """)
  ratings_above_two = cur.fetchall()
  count_ratings_above_two_imdb = len(ratings_above_two)
  count_ratings_above_two_imdb = int(count_ratings_above_two_imdb)
  return count_ratings_above_two_imdb




def calculate_percentage_rating_above_two_metacritic(cur):
  cur.execute("""
      SELECT metacritic FROM Movie_Ratings WHERE metacritic > 2.0 AND metacritic IS NOT NULL
  """)
  ratings_above_two = cur.fetchall()
  count_ratings_above_two_metacritic = len(ratings_above_two)
  count_ratings_above_two_metacritic = int(count_ratings_above_two_metacritic)
  return count_ratings_above_two_metacritic




def write_calculated_data(average_imdb_ratings, average_rotten_tom_ratings, average_metacritic_ratings, count_ratings_above_two_imdb, count_ratings_above_two_metacritic):
  with open('calculated_data.txt', 'a') as f:
      f.write("Average Rating for IMDB: {:.2f}\n".format(average_imdb_ratings))
      f.write("Average Rating for Rotten Tomatoes: {:.2f}\n".format(average_rotten_tom_ratings))
      f.write("Average Rating for Metacritic: {:.2f}\n".format(average_metacritic_ratings))
      f.write(" Percent of Ratings Above Two for IMDB: {:.2f}\n".format(count_ratings_above_two_imdb))
      f.write(" Percent of Ratings Above Two for Metacritic: {:.2f}\n".format(count_ratings_above_two_metacritic))




def fetch_movie_ratings(cur):
  cur.execute("SELECT imdb, rotten_tomatoes FROM Movie_Ratings WHERE imdb IS NOT NULL AND rotten_tomatoes IS NOT NULL")     
  return cur.fetchall()




def calculate_regression_line(x, y):
  coef = np.polyfit(x, y, 1)
  return coef




def scatter_plot(imdb_ratings, rotten_tomatoes_ratings):
  print(imdb_ratings)
  plt.figure(figsize=(8, 6))
  plt.scatter(imdb_ratings, rotten_tomatoes_ratings, c='hotpink', alpha=0.7)
  coef = calculate_regression_line(imdb_ratings, rotten_tomatoes_ratings)
  plt.plot(np.array(imdb_ratings), np.polyval(coef, np.array(imdb_ratings)), color='#6495ED')
  plt.xlabel('IMDB Ratings')
  plt.ylabel('Rotten Tomatoes Ratings')
  plt.title('IMDB Average ratings vs Rotten Tomatoes Average Ratings')
  plt.grid(True)
  plt.tight_layout()
  plt.show()




def fetch_ratings_genres_and_names(cur):
  cur.execute("""
      SELECT m.genre_id, g.genre, m.imdb, m.rotten_tomatoes, m.metacritic
      FROM Movie_Ratings AS m
      JOIN Categories AS g ON m.genre_id = g.genre_id
  """)
  return cur.fetchall()




def calculate_average_ratings_by_genre(ratings_genres_and_names):
  avg_ratings_by_genre = {}
  count_by_genre = {}


  for genre_id, genre, imdb, rotten_tomatoes, metacritic in ratings_genres_and_names:
      if genre not in avg_ratings_by_genre:
          avg_ratings_by_genre[genre] = [0, 0, 0]
          count_by_genre[genre] = 0
      if imdb is not None:
          avg_ratings_by_genre[genre][0] += imdb
      if rotten_tomatoes is not None:
          avg_ratings_by_genre[genre][1] += rotten_tomatoes
      if metacritic is not None:
          avg_ratings_by_genre[genre][2] += metacritic
      count_by_genre[genre] += 1


  for genre in avg_ratings_by_genre:
      if count_by_genre[genre] != 0:
          avg_ratings_by_genre[genre][0] /= count_by_genre[genre]
          avg_ratings_by_genre[genre][1] /= count_by_genre[genre]
          avg_ratings_by_genre[genre][2] /= count_by_genre[genre]


  return avg_ratings_by_genre




def grouped_bar_chart(avg_ratings_by_genre):
  genres = list(avg_ratings_by_genre.keys())
  num_genres = len(genres)
  imdb_ratings = [avg_ratings_by_genre[genre][0] for genre in genres]
  rotten_tomatoes_ratings = [avg_ratings_by_genre[genre][1] for genre in genres]
  metacritic_ratings = [avg_ratings_by_genre[genre][2] for genre in genres]


  index = np.arange(num_genres)
  bar_width = 0.25
  plt.figure(figsize=(8, 6))
  plt.bar(index, imdb_ratings, bar_width, label='IMDB', color = '#FF69B4')
  plt.bar(index + bar_width, rotten_tomatoes_ratings, bar_width, label='Rotten Tomatoes', color = '#9DC183')
  plt.bar(index + 2 * bar_width, metacritic_ratings, bar_width, label='Metacritic', color = '#6495ED')
  plt.xlabel('Genre')
  plt.ylabel('Average Rating')
  plt.title('Average Movie Ratings by Genre and Website')
  plt.xticks(index + bar_width, genres, rotation=45, ha='right')
  plt.legend()
  plt.tight_layout()
  plt.show()






def main ():
   conn = sqlite3.connect('complete.db')
   cursor = conn.cursor()
   average_rating_imdb = calculate_average_rating_imdb(cursor)
   average_rating_rotten_tomatoes = calculate_average_rating_rotten_tomatoes(cursor)
   average_rating_rotten_metacritic = calculate_average_rating_metacritic(cursor)
   percentage_rating_above_two_imdb = calculate_percentage_rating_above_two_imdb(cursor)
   percentage_rating_above_two_metacritic = calculate_percentage_rating_above_two_metacritic(cursor)


   write_calculated_data(average_rating_imdb, average_rating_rotten_tomatoes, average_rating_rotten_metacritic, percentage_rating_above_two_imdb, percentage_rating_above_two_metacritic)


   ratings = fetch_movie_ratings(cursor)
   imdb_ratings = [rating[0] for rating in ratings]
   rotten_tomatoes_ratings = [rating[1] for rating in ratings]
   scatter_plot(imdb_ratings, rotten_tomatoes_ratings)


   ratings_genres_and_names = fetch_ratings_genres_and_names(cursor)
   avg_ratings_by_genre = calculate_average_ratings_by_genre(ratings_genres_and_names)
   grouped_bar_chart(avg_ratings_by_genre)


conn.close()






if __name__ == "__main__":
      main()