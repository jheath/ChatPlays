import sys
import random
import json


# TODO: variable names are inconsistent, needs cleanup
# var inits
debug = False
# define input arguments
argCount = len(sys.argv)
args = sys.argv
curUser = args[1]
action = args[2]
if len(args) > 3:
    targets = args[3]

# this value is not case sensitive somehow
heldValues = ["Not Held", "Held"]
rollsleft = 3
# dice[number][held value,dice value]
dice = [[heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0]]

# TODO: this should be a function
# Open history file
historyFile = "history.json"
file = open(historyFile, "r")
filedata = file.read()
history = json.loads(filedata)

# TODO: check for matching user data before processing

# TODO: this should be a function
# update roll from history
if debug:
    print(str(history[str(curUser)]["current"]["remainingRolls"]))
rollsleft = history[str(curUser)]["current"]["remainingRolls"]

if debug:
    print("debug-rollsleft:" + str(rollsleft) + "\n")
for thing in range(5):
    diceField = "dice" + str(thing + 1)
    # if dice[int(thing)][1] == 0:

    # read state for player's dice
    diceKeep = history[str(curUser)]["current"][str(diceField) + "Held"]
    diceValue = history[str(curUser)]["current"][str(diceField)]
    dice[thing][0] = str(diceKeep)
    dice[thing][1] = str(diceValue)

    if debug:
        print("dice#: " + str(thing + 1))
        print("value: " + str(diceValue))
        print("hold: " + str(diceKeep))
        print("alldice: " + str(dice))
        print("thisdice: " + str(dice[thing]))
        print("dice1val: " + str(dice[thing][1]))
        print(history[str(curUser)]["current"]["dice" + str(thing + 1)] + " - no match")
        print("\n")


# initialize dice
def initial_roll():
    for die in range(5):
        dice[die][1] = random.randrange(1, 7)
        die += 1
    reducerolls()


# Game loop
def main_loop():
    # split args and run function on each
    if debug:
        print("rollsleft2: " + str(rollsleft))
        print("roll action:" + str(action))
        print("roll lef:" + str(rollsleft))
        print("action:" + str(action) + "   " + (rollsleft))
    if action == "keep" or action == "drop":
        dicechange()
        score_roll()

    elif action == "roll":
        if debug:
            print("rollsleft-roll: " + str(rollsleft))
        if rollsleft == 3:
            initial_roll()
        elif int(rollsleft) > 0:
            user_check_dice()
            reducerolls()
            score_roll()
            print("Rolls remaining: " + str(rollsleft))

    elif action == "status":
        score_roll()
        print("Rolls remaining: " + str(rollsleft))

    else:
        print("Invalid action specified.")

    # reset if this roll was the last remaining
    if debug:
        print("rollsleft1: " + str(rollsleft))
    if rollsleft == 0:
        # score_roll()
        resetrolls()
        resethelds()
        if debug:
            print("rollsleft2: " + str(rollsleft))

    writehistory()


def dicechange():
    if debug:
        print("write dice change")
        print(len(args))
    if action == "keep" or action == 'drop':
        if len(args) > 3:
            holdnum = args[3].split(",")
        for y in holdnum:
            if debug:
                print("holdnum:" + str(holdnum))
                print("y: " + str(y))
                print(diceField)
            # index out of range
            if int(y) < 6:
                if dice[int(y)][0] == 0:
                    # history[str(curUser)]["current"]["disk" + str(y) + "held"] = 0
                    dice[int(y)][0] = 1
                else:
                    dice[int(y)][0] = 0


def writehistory():
    # not sure if this prints dice or history or bothkj
    print("write history")


# Let users hold dice
def user_check_dice():
    for x in range(5):
        if debug:
            print("x: " + str(x))
        # print('Dice #' + str(x + 1) + ': ' + str(dice[x][1]) + '   ' + str(dice[x][0]))
        reroll()
        x += 1


def reroll():
    for x in range(5):
        if dice[x][0] == heldValues[0]:
            dice[x][1] = random.randrange(1, 7)
        if debug:
            print("heldValues-reroll: " + str(heldValues[0]) + " " + str(dice[x][0]))
            print("reduce")
            print("xreroll: " + str(x))

    # reducerolls()


def reducerolls():
    global rollsleft
    if debug:
        print("rollsleft-reduce=" + str(rollsleft))
    rollsleft = int(rollsleft) - 1
    if debug:
        print("rollsleft-reduce=" + str(rollsleft))


def resetrolls():
    global rollsleft
    rollsleft = 3


def resethelds():
    for x in range(5):
        dice[x][0] = heldValues[0]


def score_roll():
    score = 0
    special = ""
    num1 = 0
    num2 = 0
    num3 = 0
    num4 = 0
    num5 = 0
    num6 = 0

    for x in range(5):
        # if debug:
        print('Dice #' + str(x + 1) + ': ' + str(dice[int(x)][1]) + "    " + str(dice[int(x)][0]))

    # check for yahtzee
    if dice[0][1] == dice[1][1] and dice[1][1] == dice[2][1] and dice[2][1] == dice[3][1] and dice[3][1] == dice[4][1]:
        score = 50
        special = "! YAHTZEE !"

    # check for straights
    for x in range(5):
        if dice[x][1] == 1:
            num1 += 1
        elif dice[x][1] == 2:
            num2 += 1
        elif dice[x][1] == 3:
            num3 += 1
        elif dice[x][1] == 4:
            num4 += 1
        elif dice[x][1] == 5:
            num5 += 1
        elif dice[x][1] == 6:
            num6 += 1

    # Large Straight check
    if (num1 > 0 and num2 > 0 and num3 > 0 and num4 > 0 and num5 > 0) or (
            num2 > 0 and num3 > 0 and num4 > 0 and num5 > 0 and num6 > 0):
        score = 40
        special = "STRAIGHT"

    # Small Straight check
    if score == 0 and (
            (num1 > 0 and num2 > 0 and num3 > 0 and num4 > 0)
            or (num2 > 0 and num3 > 0 and num4 > 0 and num5 > 0)
            or (num3 > 0 and num4 > 0 and num5 > 0 and num6 > 0)):
        score = 30
        special = "straight"
    if score == 0:
        for x in range(5):
            score += int(dice[x][1])

    # check for full house and set to 25 if it is less than the current score
    if score < 25:
        fullhouse = "FULL HOUSE"
        if num1 == 3 and (num2 == 2 or num3 == 2 or num4 == 2 or num5 == 2 or num6 == 2):
            score = 25
            special = fullhouse
        elif num2 == 3 and (num1 == 2 or num3 == 2 or num4 == 2 or num5 == 2 or num6 == 2):
            score = 25
            special = fullhouse
        elif num3 == 3 and (num1 == 2 or num2 == 2 or num4 == 2 or num5 == 2 or num6 == 2):
            score = 25
            special = fullhouse
        elif num4 == 3 and (num1 == 2 or num2 == 2 or num3 == 2 or num5 == 2 or num6 == 2):
            score = 25
            special = fullhouse
        elif num5 == 3 and (num1 == 2 or num2 == 2 or num3 == 2 or num4 == 2 or num6 == 2):
            score = 25
            special = fullhouse
        elif num6 == 3 and (num1 == 2 or num2 == 2 or num3 == 2 or num4 == 2 or num5 == 2):
            score = 25
            special = fullhouse

    # TODO:4 of a kind
    # TODO:3 of a kind

    print("")
    if special != "":
        print("** " + special + " **")
    print('Your score = ' + str(score))


main_loop()
