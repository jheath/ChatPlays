import os
import sys
from datetime import date
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
            print("Game still in progress.")
            sys.exit(1)

        # Reset the round scores each rounds score will be appended here
        self._set_round_scores([])

        # Setting to 2 remaining rolls here because the first roll is in progress
        self._set_remaining_rolls(2)

        # Rolls the dice to start things off
        self.dice.roll()
        self._set_dice(self.dice.get_dice_values())

        self._save_state()

        return self.history.data[self.username]

    def roll(self):
        if self._get_remaining_rolls() == 0:
            print("No rolls remaining.")
            sys.exit(1)

        # Any dice not held wwill have it's value set to 0 for the roll
        newDice = [value if index + 1 in self._get_dice_held() else 0 for index, value in enumerate(self._get_dice())]
        self.dice.update_dice(newDice)

        # Roll the dice
        self.dice.roll()
        self._set_dice(self.dice.get_dice_values())

        # Decrement the remaining rolls
        self._set_remaining_rolls(self._get_remaining_rolls() - 1)

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

            # End of game
            if len(self._get_round_scores()) == 3:
                # Sum the round scores to get the total score
                total_score = sum(self.history.data[self.username]['current']['roundScores'])
                self.history_highscore.submit_score(self.username, total_score)

        self._save_state()

        return self.history.data[self.username]

    def hold(self, dice_to_hold):
        if self._get_remaining_rolls() == 0:
            print("No rolls remaining.")
            sys.exit(1)

        # Set the dice to hold
        self._set_dice_held(dice_to_hold)

        self._save_state()

        return self.history.data[self.username]

    def status(self):
        return self.history.data[self.username]

    def end_round(self):
        # Check that we are not already ended.
        if self._get_remaining_rolls() == 0:
            print("No more remaining rolls.")
            sys.exit(1)

        ### I'm getting tired, this is probably a dumb way to do this
        # Set remaining rolls to 1 (to be the last roll)
        self._set_remaining_rolls(1)

        # Hold all dice, for the roll
        self._set_dice_held([1,2,3,4,5])
        self.roll()

    def get_dice_values(self):
        return self.dice.get_dice_values()

    def get_score(self):
        return self.dice.get_score()

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
