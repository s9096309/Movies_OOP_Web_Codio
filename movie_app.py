import requests
import os
import statistics
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
import random

load_dotenv()

class MovieApp:
    """
    A class to manage a movie application.
    """

    def __init__(self, storage):
        """
        Initializes the MovieApp with a storage object and API key.

        Args:
            storage (Storage): The storage object for movie data.
        """
        self._storage = storage
        self.api_key = os.getenv("OMDB_API_KEY")

    def _extract_year(self, year_str):
        """
        Extracts the year from a year string.

        Args:
            year_str (str): The year string to extract from.

        Returns:
            int: The extracted year, or None if invalid.
        """
        try:
            return int(year_str.split('–')[0])
        except ValueError:
            print(f"Invalid year format: {year_str}")
            return None

    def _command_list_movies(self):
        """Lists all movies in the storage."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            return
        for title, movie in movies.items():
            year = movie['year']
            rating = movie['rating']
            poster_url = movie['poster_url']
            if poster_url:
                print(f"{title}: {rating} ({year}) - Poster: {poster_url}")
            else:
                print(f"{title}: {rating} ({year}) - Poster: None")

    def _command_add_movie(self):
        """Adds a movie to the storage using the OMDb API."""
        title = input("Enter the movie title: ")
        if not self.api_key:
            print("Error: OMDB API key is missing!")
            return

        url = f"http://www.omdbapi.com/?apikey={self.api_key}&t={title}"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            if data['Response'] == 'True':
                movie_title = data['Title']
                year_str = data['Year']
                year = self._extract_year(year_str)
                if year is None:
                    return
                rating = float(data['imdbRating']) if data['imdbRating'] != 'N/A' else 0.0
                poster_url = data['Poster'] if data['Poster'] != 'N/A' else None
                imdbID = data['imdbID'] if data['imdbID'] else 'No IMDb ID available'

                self._storage.add_movie(movie_title, year, rating, poster_url, imdbID)
                print(f"Movie '{movie_title}' added successfully!")
            else:
                print(f"Error: {data['Error']}")
        except requests.exceptions.RequestException as e:
            print(f"Error: Could not connect to OMDb API: {e}")
        except ValueError as e:
            print(f"Error: Could not decode JSON response: {e}")

    def _command_delete_movie(self):
        """Deletes a movie from the storage."""
        title = input("Enter movie title to delete: ")
        self._storage.delete_movie(title)
        print(f"Movie '{title}' deleted successfully.")

    def _command_movie_stats(self):
        """Calculates and displays movie statistics."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to calculate stats.")
            return

        ratings = [movie['rating'] for movie in movies.values()]

        avg_rating = sum(ratings) / len(ratings)
        median_rating = statistics.median(ratings)
        best_movie = max(movies.items(), key=lambda item: item[1]['rating'])
        worst_movie = min(movies.items(), key=lambda item: item[1]['rating'])

        print("\nMovie Stats:")
        print(f"  Average rating: {avg_rating:.2f}")
        print(f"  Median rating: {median_rating}")
        print(f"  Best movie: {best_movie[0]}, {best_movie[1]['rating']}")
        print(f"  Worst movie: {worst_movie[0]}, {worst_movie[1]['rating']}")

    def _command_generate_website(self):
        """Generates a website from the movie data."""
        try:
            template_dir = os.path.join(os.path.dirname(__file__), "templates")
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template("index_template.html")

            movies = list(self._storage.list_movies().items())  # Get list of tuples (title, movie_data)

            if not movies:
                print("No movies to display.")
                return

            # Add 'title' key to each movie dictionary
            movie_grid = []
            for title, movie_data in movies:
                movie_data['title'] = title  # Add the title to the dictionary
                movie_grid.append(movie_data)

            html_content = template.render(title="My Movie App", movie_grid=movie_grid)

            with open(os.path.join(template_dir, "index.html"), "w", encoding="utf-8") as output_file:
                output_file.write(html_content)

            print("Website was generated successfully.")

        except FileNotFoundError:
            print("Error: index_template.html not found. Make sure the template file exists.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _command_random_movie(self):
        """Selects and displays a random movie."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in the database.")
            return

        random_movie_title = random.choice(list(movies.keys()))
        random_movie = movies[random_movie_title]

        print(f"Your movie for tonight: {random_movie_title}, it's rated {random_movie['rating']}")

    def _command_search_movie(self):
        """Searches for movies by title."""
        search_term = input("Enter search term: ").lower()
        movies = self._storage.list_movies()
        found_movies = []
        for title, movie in movies.items():
            if search_term in title.lower():
                found_movies.append((title, movie))
        if found_movies:
            print("Found movies:")
            for title, movie in found_movies:
                print(f"{title}: {movie['rating']} ({movie['year']})")
        else:
            print("No movies found.")

    def _command_sort_movies(self):
        """Sorts movies by rating."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to sort.")
            return

        order = input("Sort order (A/D): ").upper()
        if order not in ('A', 'D'):
            print("Invalid order. Using ascending order.")
            order = 'A'

        sorted_movies = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=(order == 'D'))

        print("Sorted movies:")
        for title, movie in sorted_movies:
            print(f"{title}: {movie['rating']} ({movie['year']})")

    def run(self):
        """Runs the movie application."""
        while True:
            print("\n*** Movie App Menu ***")
            print("1. List movies")
            print("2. Add movie")
            print("3. Delete movie")
            print("4. Movie stats")
            print("5. Generate website")
            print("6. Random movie")
            print("7. Search movie")
            print("8. Movies sorted by rating")
            print("0. Exit")

            choice = input("Enter your choice (0-8): ")
            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_movie_stats()
            elif choice == "5":
                self._command_generate_website()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_sort_movies()
            elif choice == "0":
                print("Exiting the movie app.")
                break
            else:
                print("Invalid choice, please try again.")