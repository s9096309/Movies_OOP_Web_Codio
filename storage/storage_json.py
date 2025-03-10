import json
import os

class StorageJson:
    def __init__(self, filename):  # entfernt Standardwert
        self.filename = filename
        storage_dir = os.path.dirname(self.filename)
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        if not os.path.exists(self.filename):
            self._save_movies({})

    def _save_movies(self, movies):
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(movies, file, indent=4)
        except IOError as e:
            print(f"Error saving to file {self.filename}: {e}")

    def list_movies(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                movies = json.load(file)
        except FileNotFoundError:
            print(f"File not found: {self.filename}")
            movies = {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {self.filename}: {e}")
            movies = {}
        except Exception as e:
            print(f"An unexpected error occurred while listing movies: {e}")
            movies = {}
        return movies

    def add_movie(self, title, year, rating, poster_url, imdb_id):
        movies = self.list_movies()
        if any(movie.get("imdb_id") == imdb_id for movie in movies.values()):
            print(f"Movie '{title}' is already in the database.")
            return False

        movies[title] = {
            "year": year,
            "rating": rating,
            "poster_url": poster_url,
            "imdb_id": imdb_id
        }
        self._save_movies(movies)
        return True

    def delete_movie(self, title):
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            return True  # Movie deleted successfully
        else:
            print(f"The movie '{title}' was not found.")
            return False  # Movie not found

    def update_movie(self, title, new_title, new_year, new_rating):
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
            self._save_movies(movies)
        else:
            print(f"Movie '{title}' not found in the database.")