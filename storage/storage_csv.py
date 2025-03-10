import os
import csv

class StorageCsv:
    def __init__(self, file_path="storage/movies.csv"):
        self.file_path = file_path

    def list_movies(self):
        movies = {}
        try:
            with open(self.file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row:  # Check if row is not empty
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
                return True  # Movie deleted successfully
            else:
                print(f"Movie '{title}' not found in the database.")
                return False  # Movie not found
        except Exception as e:
            print(f"An error occurred while deleting the movie: {e}")
            return False  # Error occurred

    def update_movie(self, title, new_title, new_year, new_rating):
        try:
            movies = self.list_movies()
            if title in movies:
                # If the title is being updated, delete the old entry
                if title != new_title:
                    del movies[title]

                movies[new_title] = {
                    'year': new_year,
                    'rating': new_rating,
                    'poster_url': movies[title]['poster_url'],  # Keep the original poster URL
                    'imdb_id': movies[title]['imdb_id']  # Keep the original IMDB ID
                }
                with open(self.file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Year', 'Rating', 'Poster URL', 'IMDB ID'])
                    for title, movie in movies.items():
                        writer.writerow([title, movie['year'], movie['rating'], movie['poster_url'], movie['imdb_id']])
            else:
                print(f"Movie '{title}' not found in the database.")
        except Exception as e:
            print(f"An error occurred while updating the movie: {e}")