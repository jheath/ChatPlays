import sys
import random
import os.path
import json

debug = False
# TODO: variable names are inconsistent, needs cleanup
# define input arguments
args = sys.argv
curUser = args[1]
action = args[2]
if len(args) > 3:
    targets = args[3]

# var inits
# This template is used to add new users to the history file
template = """
    "current": {
        "remainingRolls": "3",
        "dice1": "0",
        "dice2": "0",
        "dice3": "0",
        "dice4": "0",
        "dice5": "0",
        "dice1Held": "Not Held",
        "dice2Held": "Not Held",
        "dice3Held": "Not Held",
        "dice4Held": "Not Held",
        "dice5Held": "Not Held"
    },
    "daily": {
        "score": "0",
        "numGames": "0"
    },
    "top": {
        "score": "0",
        "numGames": "0"
    }
}"""

# blank entry for top scores
# write this first to finish file without ','
# or figure out the syntax for adding this to the main dict
top_record = """\n"top": {
    "daily": {
        "players": "1",
        "numUsers": "1",
        "user": \"""" + curUser + """\",
        "score": "0"
    },
    "all": {
        "numGames": "1",
        "numUsers": "1",
        "user": \"""" + curUser + """\",
        "score": "0"
    }
}
}"""

#if debug:
    # print("")
    # print("top:\n"+top_record)

heldValues = ["Not Held", "Held"]
rollsleft = 4
historyFile = "history.json"
bakFile = historyFile + ".bak"

# brand new history file
historyEntry="\n" + "{\n\"" + str(curUser) + "\": {" + template + top_record
if debug:
    print("")
    print("tmp new historyEntry:"+historyEntry )

# TODO: double check this
# create empty history record in json format
# history=json.loads(historyEntry)

dice = [[heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0]]


def open_history():
    # existing file data
    global filedata
    global history
    global historyEntry
    global rollsleft
    if debug:
        print("start open_history")
    historyFile = "history.json"
    template = """
        "current": {
            "remainingRolls": "3",
            "dice1": "0",
            "dice2": "0",
            "dice3": "0",
            "dice4": "0",
            "dice5": "0",
            "dice1Held": "Not Held",
            "dice2Held": "Not Held",
            "dice3Held": "Not Held",
            "dice4Held": "Not Held",
            "dice5Held": "Not Held"
        },
        "daily": {
            "score": "0",
            "numGames": "0"
        },
        "top": {
            "score": "0",
            "numGames": "0"
        }
    }"""

    # only run history pull if this file exists
    if os.path.isfile(historyFile):
        # Open history file
        if debug:
            print("historyFile: " + historyFile)
            print("-historyFile exists")

        file = open(historyFile, "r")
        filedata = file.read()
        file.close()
        history = json.loads(filedata)

        if debug:
            print("filedata: " + str(filedata))
            print("-history:" + str(history))

        # TODO: should be a function
        # check_for_user()
        # see if curUser is in history
        userExists = False
        for key in history.keys():
            if debug:
                print("history key:" + str(key))
                print("user:"+curUser)
            if key == curUser:
                if debug:
                    print("found "+key+":"+curUser)
                userExists = True
                break

        if userExists == False:
            # TODO: should be a function
            # new_user()
            # user not found,add new key to history
            if debug:
                print("user not found in history - "+curUser)

            userTemplate  = "{ " + curUser + ": { "+ template + " }"
            history.update(userTemplate)
            # This creates a new key with the default fields

            history[curUser] = template

            # historyEntry = "\n{\n\"" + str(curUser) + "\": {" + template + "\n"+ str(filedata[2:])
        else:
            # TODO: this should be a function
            # found_user()
            # user does exist, update history dict values

            for x in range(5):
                diceNum = "dice"+str(x+1)
                diceHold = "dice"+str(x+1)+"Held"
                # find dice value
                dice[x][1] = history[curUser]["current"][diceNum]
                dice[x][0] = history[curUser]["current"][diceHold]
                if debug:
                    print(diceNum + ":" + dice[x][1])
                    print(diceHold + ":" + dice[x][0])
                # die += 1

            rollsleft = history[curUser]["current"]["remainingRolls"]


def initial_roll():
    # initialize dice
    if debug:
        print("running initial_roll sub")

    for die in range(5):
        dice[die][1] = random.randrange(1, 7)
        die += 1

    reducerolls()


# Game loop
def main_loop():
    # split args and run function on each

    # checking for history file
    # reading history file, creating copy
    # building new player records
    open_history()

    if debug:
        print("")
        print("roll action:" + str(action))
        print("rolls remaining:" + str(rollsleft))
        print("action:" + str(action) + "   " + str(rollsleft))

    if action.lower() == "keep" or action == "drop":
        dicechange()
        score_roll()

    elif action.lower() == "roll":
        if debug:
            print("roll sub")

        if int(rollsleft) == 4:
            initial_roll()
            reducerolls()
            score_roll()
        elif int(rollsleft) in [1, 2, 3]:
            user_check_dice()
            reducerolls()
            score_roll()
            print("Rolls remaining: " + str(rollsleft))

    elif action.lower() == "status":
        if debug:
            # the history data isn't read yet
            print("rollsleft:" + str(rollsleft))

        if int(rollsleft) in [1, 2, 3]:
            score_roll()
        elif rollsleft == 4:
            print("You haven't rolled yet.\n")

        print("Rolls remaining: " + str(rollsleft))

    else:
        print("")
        print("Invalid action specified.")

    # reset if this roll was the last remaining
    if debug:
        print("")
        print("rollsleft1: " + str(rollsleft))
    if rollsleft == 0:
        # score_roll()
        resetrolls()
        resethelds()
        if debug:
            print("")
            print("rolls and helds reset: " + str(rollsleft))

    if action != "status":
        writehistory()


def writehistory():
    # this should just be adding/updating a key in a dict
    # but cant remember how this works anymore
    # probably a simple fix

    global history
    global historyFile
    global historyEntry

    # TODO: update history with new dice values
    x = 1
    while x != 6:
        #update history with dice

        dicefield = "dice"+str(x)
        diceheld = dicefield + "held"
        if debug:
            print(str(x)+":"+str(dice[x][1]))

        heldstr = str(dice[x][0])

        if heldstr == "Held":
            history[curUser]["current"][dicefield] = str(dice[x][1])
            history[curUser]["current"][diceheld] = str(dice[x][0])

        x += 1
        # print("")

    # Convert python to json
    historyJson = json.dumps(history, indent = 4)

    # write new history file
    file = open(historyFile, "w")
    file.write(str(historyJson))
    file.close()


def dicechange():
    if debug:
        print("--dicechange--")
        print("")
        print("argument count:" + str(len(args)))
    if action == "keep" or action == 'drop':
        # seems like a dupe
        if len(args) > 3:
            holdnum = args[3].split(",")

        for y in holdnum:
            if debug:
                print("")
                print("holdnum:" + str(holdnum))
                print("y: " + str(y))
                # print("dice field: " + str(diceField))

            if int(y) < 6:
                if debug:
                    print("")
                    print("dice #1: " + str(y))
                    print("dice all1: " + str(dice))
                    print("hold value1: " + str(dice[int(y) - 1]))

                if action.lower() == "keep":
                    dice[(int(y) - 1)][0] = heldValues[1]
                elif action.lower() == "drop":
                    dice[(int(y) - 1)][0] = heldValues[0]
                else:
                    print("didn't match keep/drop")

                if debug:
                    print("")
                    print("hold value2: " + str(dice[int(y) - 1]))
                    print("hold: " + str(dice[int(y)][0]))
                    print("value: " + str(dice[int(y)][1]))
                    print("dice all2: " + str(dice))
                    print("--dicechange--")


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
            print("xreroll: " + str(x))


def reducerolls():
    global rollsleft

    rollsleft = int(rollsleft) - 1
    if debug:
        print("rollsleft-reduce=" + str(rollsleft))


def resetrolls():
    global rollsleft
    rollsleft = 4


def resethelds():
    for x in range(5):
        dice[x][0] = heldValues[0]


def score_roll():
    # only run this when rollsLeft == 0?
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
