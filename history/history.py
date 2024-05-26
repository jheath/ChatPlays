import json
import os
import sys

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
    - get_top(): Returns data for the leaderboard.

    Example usage:
    history = History()
    history.load_file('../history.json')
    //do something with history
    history.save_file()
    """

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'history.json')
        self.data = self.load_file(self.file_path)

    def load_file(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

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

    def get_top(self):
       return self.data['top']
