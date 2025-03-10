import os
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app import MovieApp

def main():
    username = input("Enter your username: ")
    filename = os.path.join("storage", f"{username}.csv")

    # Create the 'storage' directory if it doesn't exist
    if not os.path.exists("storage"):
        os.makedirs("storage")

    # Check if the file exists, and create it if not
    if not os.path.exists(filename):
        # Create an empty file
        with open(filename, 'w') as f:
            pass

    storage = StorageCsv(filename)
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()