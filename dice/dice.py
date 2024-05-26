import random
import json

class Dice:
    """
    Class representing a set of dice for yaht-sea.

    Attributes:
    - dice (list): A list containing the current values of the dice. [5,4,3,2,1] //omg straight

    Methods:
    - __init__(initial_dice=None): Initializes a new Dice instance with optional initial dice values.
    - roll(): Rolls the dice, generating random values for any dice that are currently showing 0.
    - get_dice_values(): Returns the current values of the dice.
    - get_score(): Calculates the score based on the current values of the dice.
    - reset(): Resets dice to default values. [0,0,0,0,0]

    Example usage:
    dice = Dice()
    dice.roll()
    print("Dice values:", dice.get_dice_values())
    print("Score:", dice.get_score())

    Example usage (holding dice):
    dice = Dice([0,1,0,1,0])
    dice.roll() // only 0 will reroll
    print("Dice values:", dice.get_dice_values())
    """

    def __init__(self, initial_dice=None):
       if initial_dice is None:
           initial_dice = [0,0,0,0,0]
       self.dice = initial_dice

    def roll(self):
        self.dice = [random.randint(1, 6) if value == 0 else value for value in self.dice]

    def get_dice_values(self):
        return self.dice

    def get_score(self):
        counts = [self.dice.count(value) for value in set(self.dice)]

        def is_consecutive(length):
            sorted_dice = sorted(set(self.dice))
            for i in range(len(sorted_dice) - length + 1):
                if sorted_dice[i:i + length] == list(range(sorted_dice[i], sorted_dice[i] + length)):
                    return True
            return False

        if 5 in counts:
            return ['Yaht-sea', 50]
        elif is_consecutive(5):
            return ['Large straight', 40]
        elif is_consecutive(4):
            return ['Small straight', 30]
        elif 3 in counts and 2 in counts:
            return ['Full house', 25]
        elif 4 in counts:
            return ['Four of a kind', sum([value for value in self.dice if self.dice.count(value) >= 4])]
        elif 3 in counts:
            return ['Three of a kind', sum([value for value in self.dice if self.dice.count(value) >= 3])]
        else:
            return ['None', 0]

    def reset(self):
        self.dice = [0,0,0,0,0]

    def update_dice(self, dice):
        self.dice = dice

    def to_dictionary(self):
        return {'dice': self.dice}
