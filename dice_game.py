import sys
import random

# var inits
dice = [0, 0, 0, 0, 0]
diceHeld = ["Not Held", "Not Held", "Not Held", "Not Held", "Not Held"]
rollsLeft = 3
gameState = "new roll"
userScore = 0
playing = True


# initialize dice
def initial_roll():
    for die in range(5):
        dice[die] = random.randrange(1, 7)
        die = die + 1
        continue
    reduceRolls()


# Game loop
def main_loop():
    while playing == True:
        if rollsLeft == 3:
            initial_roll()
        elif rollsLeft > 0:
            user_check_dice()
            reroll()
        else:
            score_roll()
            val = input('Play again?(y or n)\n')
            if val == 'n':
                playing == False
                break
            else:
                resetRolls()
                resetHelds()


# Let users hold dice
def user_check_dice():
    userDone = False
    while (userDone == False):
        for x in range(5):
            print('Dice #' + str(x + 1) + ': ' + str(dice[x]) + '   ' + diceHeld[x])
        # print('Type the number of the die to hold it or type C to continue.')
        val = input('Type the number of the die to hold it or type C to continue.\n')

        if val == "C" or val == 'c':
            userDone = True
        elif val == "1" or val == "2" or val == "3" or val == "4" or val == "5":
            if diceHeld[int(val) - 1] == "Not Held":
                diceHeld[int(val) - 1] = "Held"
            else:
                diceHeld[int(val) - 1] = "Not Held"


def reroll():
    for x in range(5):
        if diceHeld[x] == "Not Held":
            dice[x] = random.randrange(1, 7)
            continue
    reduceRolls()


def reduceRolls():
    global rollsLeft
    rollsLeft -= 1


def resetRolls():
    global rollsLeft
    rollsLeft = 3


def resetHelds():
    global diceHeld
    for x in range(5):
        diceHeld[x] = "Not Held"


def score_roll():
    score = 0
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    num6 = 0
    for x in range(5):
        print('Dice #' + str(x + 1) + ': ' + str(dice[x]))

    # check for yahtzee
    if dice[0] == dice[1] and dice[1] == dice[2] and dice[2] == dice[3] and dice[3] == dice[4]:
        score = 50

    # check for straights
    for x in range(5):
        if dice[x] == 1:
            num1 += 1
        elif dice[x] == 2:
            num2 += 1
        elif dice[x] == 3:
            num3 += 1
        elif dice[x] == 4:
            num4 += 1
        elif dice[x] == 5:
            num5 += 1
        elif dice[x] == 6:
            num6 += 1

    # Large Straight check
    if (num1 > 0 and num2 > 0 and num3 > 0 and num4 > 0 and num5 > 0) or (
            num2 > 0 and num3 > 0 and num4 > 0 and num5 > 0 and num6 > 0):
        score = 40

    # Small Straight check
    if score == 0 and (
            (num1 > 0 and num2 > 0 and num3 > 0 and num4 > 0)
            or (num2 > 0 and num3 > 0 and num4 > 0 and num5 > 0)
            or (num3 > 0 and num4 > 0 and num5 > 0 and num6 > 0)):
        score = 30

    if score == 0:
        for x in range(5):
            score += dice[x]

    # check for full house and set to 25 if it is less than the current score
    if score < 25:
        if num1 == 3 and (num2 == 2 or num3 == 2 or num4 == 2 or num5 == 2 or num6 == 2):
            score = 25
        elif num2 == 3 and (num1 == 2 or num3 == 2 or num4 == 2 or num5 == 2 or num6 == 2):
            score = 25
        elif num3 == 3 and (num1 == 2 or num2 == 2 or num4 == 2 or num5 == 2 or num6 == 2):
            score = 25
        elif num4 == 3 and (num1 == 2 or num2 == 2 or num3 == 2 or num5 == 2 or num6 == 2):
            score = 25
        elif num5 == 3 and (num1 == 2 or num2 == 2 or num3 == 2 or num4 == 2 or num6 == 2):
            score = 25
        elif num6 == 3 and (num1 == 2 or num2 == 2 or num3 == 2 or num4 == 2 or num5 == 2):
            score = 25

    print('Your score = ' + str(score))


main_loop()