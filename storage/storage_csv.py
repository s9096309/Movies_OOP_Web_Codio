import os
import csv

class StorageCsv:
    def __init__(self, file_path="storage/movies.csv"): #Hier anpassen
        self.file_path = file_path

    def list_movies(self):
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row:
                        title, year, rating, poster_url, imdb_id = row
                        movies[title] = {
                            'year': int(year),
                            'rating': float(rating),
                            'poster_url': poster_url,
                            'imdb_id': imdb_id
                        }
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
        return movies

    def add_movie(self, title, year, rating, poster_url, imdb_id):
        try:
            if not os.path.exists(self.file_path):
                with open(self.file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Year', 'Rating', 'Poster URL', 'IMDB ID'])

            with open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([title, year, rating, poster_url, imdb_id])
        except Exception as e:
            print(f"An error occurred while adding the movie: {e}")

    def delete_movie(self, title):
        try:
            movies = self.list_movies()
            if title in movies:
                del movies[title]
                with open(self.file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Year', 'Rating', 'Poster URL', 'IMDB ID'])
                    for title, movie in movies.items():
                        writer.writerow([title, movie['year'], movie['rating'], movie['poster_url'], movie['imdb_id']])
            else:
                print(f"Movie '{title}' not found in the database.")
        except Exception as e:
            print(f"An error occurred while deleting the movie: {e}")