from movie_app import MovieApp
from storage.storage_json import StorageJson

def main():
    username = input("Enter your username: ")
    file_path = f"{username}.json"  # Use the username to create a unique file path
    storage = StorageJson(file_path)
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()
