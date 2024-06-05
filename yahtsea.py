import os
import sys
from datetime import datetime
from history.history import History
from history.history_highscore import HistoryHighscore
from dice.dice import Dice

class YahtSea:
    """
    Class used to manage a game of YahtSea.

    Attributes:
    - username (str): The username of the player.
    - history (History): An instance of the History class to manage game history.
    - dice (Dice): An instance of the Dice class to manage dice rolls.

    Methods:
    - __init__(username): Initializes a new YahtSea instance with a given username.
    - play(): Starts a new game of YahtSea.
    - roll(): Rolls the dice.
    - hold(dice_to_hold): Holds the specified dice.
    - status(): Returns the current status of the game.
    - end_round(): Holds all dice and ends the current round.
    - get_dice_values(): Returns the current values of the dice.
    - get_score(): Returns the score of the current dice.
    - _save_state(): Saves the current state of the game.
    - _get_round_scores(): Returns the current round scores.
    - _set_round_scores(round_scores): Sets the current round scores.
    - _get_remaining_rolls(): Returns the remaining rolls in the current round.
    - _set_remaining_rolls(remaining_rolls): Sets the remaining rolls in the current round.
    - _get_dice(): Returns the current values of the dice.
    - _set_dice(dice): Sets the current values of the dice.

    Example usage:
    yahtsea = YahtSea('player1')
    yahtsea.play() //starts a game and rolls the dice
    yahtsea.hold([1,2,3]) //holds dice 1, 2, and 3
    yahtsea.roll() //rolls the dice
    yahtsea.status() //returns the current status of the game
    yahtsea.end_round() //ends the current round
    """

    def __init__(self, username):
        self.username = username
        self.history = History()
        self.history_highscore = HistoryHighscore(self.history)
        self.dice = Dice()

        # Creates a new username in the history file if it does not exist
        if self.history.does_username_exist(self.username) == False:
            self.history.create_username(self.username)

    def play(self):
        if self._get_remaining_rolls() > 0:
            return self._get_response("play", "YahtSea game already in progress.", self.history.data[self.username])

        # Set the game as started
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._set_started(date_time)
        self._set_updated(date_time)

        # Reset the round scores each rounds score will be appended here
        self._set_round_scores([])

        # Setting to 2 remaining rolls here because the first roll is in progress
        self._set_remaining_rolls(2)

        # Rolls the dice to start things off
        self.dice.roll()
        self._set_dice(self.dice.get_dice_values())

        self._save_state()

        return self._get_response("play", f"YahtSea game started. Dice values {self.history.data[self.username]['current']['dice']}", self.history.data[self.username])

    def roll(self):
        username = self.history.get_active_game_username()
        if username != self.username:
            return self._get_response("roll", "", self.history.data[self.username])

        if self._get_remaining_rolls() == 0:
            return self._get_response("roll", "No remaining rolls.", self.history.data[self.username])

        # Updated the game as being played
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._set_updated(date_time)

        self.history.get_active_game_username()

        # Any dice not held wwill have it's value set to 0 for the roll
        newDice = [value if index + 1 in self._get_dice_held() else 0 for index, value in enumerate(self._get_dice())]
        self.dice.update_dice(newDice)

        # Roll the dice
        self.dice.roll()
        self._set_dice(self.dice.get_dice_values())

        # Decrement the remaining rolls
        self._set_remaining_rolls(self._get_remaining_rolls() - 1)

        roll_status = 1

        # If we are out of rolls, log the score and reset the dice
        if self._get_remaining_rolls() == 0:
            # Sets the score for the round to the history file
            round_scores = self._get_round_scores()
            round_scores.append(self.dice.get_score()[1])
            self._set_round_scores(round_scores)

            # Reset the dice/dice held
            self.dice.reset()
            self._set_dice_held([])

            # End of round
            if len(self._get_round_scores()) < 3:
                # Reset the remaining rolls to 3 for the next round
                self._set_remaining_rolls(3)
                roll_status = 0

            # End of game
            if len(self._get_round_scores()) == 3:
                self._set_started("")
                self._set_updated("")

                # Sum the round scores to get the total score
                total_score = sum(self.history.data[self.username]['current']['roundScores'])
                self.history_highscore.submit_score(self.username, total_score)

                roll_status = -1

        self._save_state()

        data = self.history.data[self.username]

        if roll_status == 1:
            additionalInformation = f"Please hold any die you wish to keep, then roll the remaining. Rolls remaining: {data['current']['remainingRolls']}"
        elif roll_status == 0:
            additionalInformation = f"Round {len(data['current']['roundScores'])} of 3 ended. Round score: {data['current']['roundScores'][-1]}. Roll dice again to start the next round."
        else:
            additionalInformation = f"Game over! Ending score for {self.username} is {sum(data['current']['roundScores'])} points."

        return self._get_response("roll", f"Dice rolled! Dice values {self.history.data[self.username]['current']['dice']}\n{additionalInformation}", self.history.data[self.username])

    def hold(self, dice_to_hold):
        username = self.history.get_active_game_username()
        if username != self.username:
            return self._get_response("roll", "", self.history.data[self.username])

        if self._get_remaining_rolls() == 0:
            return self._get_response("hold", "No remaining rolls.", self.history.data[self.username])

        if self._get_remaining_rolls() == 3:
            return self._get_response("hold", "Roll is required to start the next round.", self.history.data[self.username])

        # Updated the game as being played
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._set_updated(date_time)

        # Set the dice to hold
        self._set_dice_held(dice_to_hold)

        self._save_state()

        return self._get_response("hold", f"YahtSea dice {dice_to_hold} have been held.", self.history.data[self.username])

    def leaderboard(self):
        date_time = datetime.now().strftime("%Y-%m-%d")

        all_users_list = [f"{user} ({score})" for user, score in self.history.data["top"]["all"]["users"].items()]
        all_users = ", " . join(all_users_list)

        daily_users_list = [f"{user} ({score})" for user, score in self.history.data["top"]["daily"][date_time].items()]
        daily_users = ", " . join(all_users_list)

        return self._get_response("status", f"Leaderboard stats. All: {all_users} Daily: {daily_users}.", self.history.data['top'])

    def resume(self):
        if self._get_remaining_rolls() == 0:
            return self._get_response("resume", "No remaining rolls.", self.history.data[self.username])

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._set_started(date_time)

        self._save_state()

        return self._get_response("status", "Game status.", self.history.data[self.username])

    def get_active_game_username(self):
        username = self.history.get_active_game_username()

        if username is not None:
            return self._get_response("get_active_game_username", f"{username}", self.history.data[self.username])
        else:
            return self._get_response("get_active_game_username", "", self.history.data[self.username])

    def end_round(self):
        username = self.history.get_active_game_username()
        if username != self.username:
            return self._get_response("roll", "", self.history.data[self.username])

        # Check that we are not already ended.
        if self._get_remaining_rolls() == 0:
            return self._get_response("play", "No remaining rolls.", self.history.data[self.username])

        data = self.history.data[self.username]

        ### I'm getting tired, this is probably a dumb way to do this
        # Set remaining rolls to 1 (to be the last roll)
        self._set_remaining_rolls(1)

        # Hold all dice, for the roll
        self._set_dice_held([1,2,3,4,5])
        self.roll()

        winner = ""
        if len(data['current']['roundScores']) == 3:
            winner = f"Game over! Ending score for {self.username} is {sum(data['current']['roundScores'])} points."
        else:
            winner = f"Round {len(data['current']['roundScores'])} of 3 ended. Round score: {data['current']['roundScores'][-1]}. Roll dice again to start the next round."

        return self._get_response("end_round", f"Round {len(data['current']['roundScores'])} of 3 ended.\n{winner}", data)


    def get_dice_values(self):
        return self.dice.get_dice_values()

    def get_score(self):
        return self.dice.get_score()

    def _set_started(self, date_time):
        self.history.data[self.username]['current']['started'] = date_time

    def _set_updated(self, date_time):
        self.history.data[self.username]['current']['updated'] = date_time

    def _save_state(self):
        self.history.save_file()

    def _get_round_scores(self):
        return self.history.data[self.username]['current']['roundScores']

    def _set_round_scores(self, round_scores):
        self.history.data[self.username]['current']['roundScores'] = round_scores

    def _get_remaining_rolls(self):
        return self.history.data[self.username]['current']['remainingRolls']

    def _set_remaining_rolls(self, remaining_rolls):
        self.history.data[self.username]['current']['remainingRolls'] = remaining_rolls

    def _get_dice(self):
        return self.history.data[self.username]['current']['dice']

    def _set_dice(self, dice):
        self.history.data[self.username]['current']['dice'] = dice

    def _get_dice_held(self):
        return self.history.data[self.username]['current']['diceHeld']

    def _set_dice_held(self, dice_held):
        self.history.data[self.username]['current']['diceHeld'] = dice_held

    def _get_response(self, action, message, data):
        return {"action": action, "message": message, "data": data}
