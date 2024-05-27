import json
import os
import sys
import shutil
from datetime import datetime

class History:
    """
    Class used to manage history. Reads and writes data to history JSON file.

    Attributes:
    - file_path (str): The path to the JSON file where data is stored.
    - data (dict): A dictionary containing the loaded data from the JSON file.

    Methods:
    - __init__: Initializes a new History instance and reads in history file.
    - load_file(file_path): Loads data from a JSON file.
    - save_file(): Saves data to the JSON file.
    - does_username_exist(key): Checks if a username exists in the data.
    - create_username(username): Creates a new username entry in the data and initializes it with default values.
	- get_active_game_username(): Returns the username of the player with the active game.

    Example usage:
    history = History()
    history.load_file('../history.json')
    //do something with history
    history.save_file()
    """

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'history.json')
        self.ensure_file_exists()
        data = self.load_file(self.file_path)
        if data is not None:
            self.data = data

    def ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            original_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'history.json.ori')
            shutil.copyfile(original_file_path, self.file_path)

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return None

    def save_file(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def does_username_exist(self, username):
        if username in self.data:
            return True
        return False

    def create_username(self, username):
        user_template = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.', 'user_template.json')
        self.data[username] = self.load_file(user_template)
        self.save_file()

	def get_active_game_username(self):
        date_time = datetime.now()

        oldest_date = None
        oldest_key = None

        for key, value in self.data.items():
            if "current" in value and "started" in value["current"] and value["current"]["started"] != "":
                game_started_date = value["current"]["started"]
                game_started_date_object = datetime.strptime(game_started_date, "%Y-%m-%d %H:%M:%S")

                game_updated_date = value["current"]["updated"]
                game_updated_date_object = datetime.strptime(game_started_date, "%Y-%m-%d %H:%M:%S")

                time_difference = date_time - game_updated_date_object

                if oldest_date is None or game_started_date < oldest_date:
                    # AFK check - 30 seconds
                    if (time_difference.total_seconds() < 180):
                        oldest_date = game_started_date
                        oldest_key = key

        return oldest_key
