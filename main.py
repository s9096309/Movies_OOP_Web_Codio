import os
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from movie_app import MovieApp

def main():
    username = input("Enter your username: ")
    filename = os.path.join("storage", f"{username}.csv")
    storage = StorageCsv(filename)
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()