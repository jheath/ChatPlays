import json
import os
import sys
import shutil
from datetime import datetime, timedelta

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

    def get_active_game_users(self):
        date_time = datetime.now()

        # Filter users based on the given rules
        valid_users = {}

        # TODO - this is an annoying hack to get around the fact that the data is not always a dictionary
        if not hasattr(self, 'data') or not isinstance(self.data, dict):
            return {}

        for key, value in self.data.items():
            if "current" in value:
                if "started" in value["current"] and value["current"]["started"] != "":
                    if "updated" in value["current"]:
                        if "remainingRolls" in value["current"]:
                            game_started_date = value["current"]["started"]
                            game_started_date_object = datetime.strptime(game_started_date, "%Y-%m-%d %H:%M:%S")

                            if value["current"]["updated"] != "":
                                game_updated_date = value["current"]["updated"]
                                game_updated_date_object = datetime.strptime(game_updated_date, "%Y-%m-%d %H:%M:%S")

                                time_difference = date_time - game_updated_date_object

                                if value["current"]["remainingRolls"] == 0 and time_difference.total_seconds() < 5:
                                    valid_users[game_started_date] = key
                                elif value["current"]["remainingRolls"] > 0 and time_difference.total_seconds() < 180:
                                    valid_users[game_started_date] = key
                            else:
                                if value["current"]["remainingRolls"] > 0:
                                    valid_users[game_started_date] = key

        return dict(sorted(valid_users.items(), key=lambda item: item[0]))

    def get_active_game_username(self):
        users = self.get_active_game_users()
        if len(users) > 0:
            return next(iter(users.values()))
        else:
            return None
