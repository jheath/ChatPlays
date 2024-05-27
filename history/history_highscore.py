import json
import os
import sys
from datetime import date

class HistoryHighscore:
    def __init__(self, history):
        self.history = history

    def submit_score(self, username, score):
        current_date = date.today().strftime("%Y-%m-%d")

        # create daily entries if they do not exist
        self.create_missing_daily_entry(current_date, username)

        # Check scores - save the score if it is the leaderboard's highest of the day
        self._update_leaderboard_scores(current_date, username, score)

        # Check user scores - save the score if it is the user's highest of the day
        self._update_user_scores(current_date, username, score)

        # Increment the number of games played
        self._increment_number_games_played(current_date, username)

        self.history.save_file()

    def create_missing_daily_entry(self, date, username):
        # TODO This needs some sort of clean up for old daily records

        # Check if the current day has a score entry for the leaderboard
        if date not in self.history.data['top']['daily']:
            self.history.data['top']['daily'][date] = {}

        # Check if the current day has a score entry for the user
        if date not in self.history.data[username]['daily']:
            self.history.data[username]['daily'][date] = {'score': 0, 'numGames': 0}

    def _update_user_scores(self, date, username, score):
        current_user_daily_score = self.history.data[username]['daily'][date]['score']

        # Only update score if it is higher than the current daily score
        if score > current_user_daily_score:
            self.history.data[username]['daily'][date]['score'] = score

        current_user_all_time_score = self.history.data[username]['top']['score']

        # Only update score if it is higher than the current all time score
        if score > current_user_all_time_score:
            self.history.data[username]['top']['score'] = score

    def _update_leaderboard_scores(self, date, username, score):
        leaderboard_scores = self.history.data['top']['daily'][date]

        if username in leaderboard_scores:
            if score > leaderboard_scores[username]:
                self.history.data['top']['daily'][date][username] = score
        else:
            # We have less then 3 scores, add the new score (assuming user is not already in the leaderboard or score is higher than existing score)
            if len(leaderboard_scores) < 3:
                # Just add the user to the leaderboard
                self.history.data['top']['daily'][date][username] = score
            else:
                # Crap, now we have to check if the user's score is higher than the lowest score in the leaderboard
                lowest_score = min(leaderboard_scores.values())
                if score > lowest_score:
                    # Remove the lowest score from the leaderboard
                    del leaderboard_scores[min(leaderboard_scores, key=leaderboard_scores.get)]
                    # Add the new score
                    self.history.data['top']['daily'][date][username] = score

        # Sort the scores
        self.history.data['top']['daily'][date] = dict(sorted(leaderboard_scores.items(), key=lambda item: item[1], reverse=True))

        # Ugh, code is not very DRY - repeat of code from above
        leaderboard_scores = self.history.data['top']['all']['users']

        if username in leaderboard_scores:
            if score > leaderboard_scores[username]:
                self.history.data['top']['all']['users'][username] = score
        else:
            # We have less then 3 scores, add the new score (assuming user is not already in the leaderboard or score is higher than existing score)
            if len(leaderboard_scores) < 3:
                # Just add the user to the leaderboard
                self.history.data['top']['all']['users'][username] = score
            else:
                # Crap, now we have to check if the user's score is higher than the lowest score in the leaderboard
                lowest_score = min(leaderboard_scores.values())
                if score > lowest_score:
                    # Remove the lowest score from the leaderboard
                    del leaderboard_scores[min(leaderboard_scores, key=leaderboard_scores.get)]
                    # Add the new score
                    self.history.data['top']['all']['users'][username] = score

        # Sort the scores
        self.history.data['top']['all']['users'] = dict(sorted(leaderboard_scores.items(), key=lambda item: item[1], reverse=True))

    def _increment_number_games_played(self, date, username):
        user_daily_games_played = self.history.data[username]['daily'][date]['numGames']
        self.history.data[username]['daily'][date]['numGames'] = user_daily_games_played + 1

        user_all_games_played = self.history.data[username]['top']['numGames']
        self.history.data[username]['top']['numGames'] = user_all_games_played + 1

        all_games_played = self.history.data['top']['all']['numGames']
        self.history.data['top']['all']['numGames'] = all_games_played + 1
