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
},"""

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

if debug:
    print("")
    # print("top:\n"+top_record)

heldValues = ["Not Held", "Held"]
rollsleft = 4
historyFile = "history.json"
bakFile = historyFile + ".bak"

historyEntry="\n" + "{\n\"" + str(curUser) + "\": {" + template + top_record
if debug:
    print("")
    print("tmp new historyEntry:"+historyEntry )

# TODO: double check this
# create empty history record in json format
history=json.loads(historyEntry)

dice = [[heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0]]


def open_history():
    # existing file data
    global filedata
    global historyEntry
    historyFile = "history.json"

    if debug:
        print("running open_history")

    # only run history pull if this file exists
    if os.path.isfile(historyFile):
        # we know there is a history file, so a backup history file should also exist
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

        # create backup file from history file
        file = open(bakFile, "w")
        file.write(str(historyEntry))
        file.close()
        if debug:
            print("backed up "+historyFile)

        # TODO: delete from json
        userExists = False
        for key in history.keys():
            if debug:
                print("history key:" + str(key))
                print("user:"+curUser)
            if key == curUser:
                userExists = True
                if debug:
                    print("found "+key+":"+curUser)
                    print("deleted historyFile[curuser]")

        if debug:
            print("finished key loop")
            print("")
            print("----++++-historyJson: "+str(history))
            # print("----++++-historyJson: "+str(history[curUser]))

        # merge the history & current roll
        if userExists == False:
            # This is a hack
            # historyEntry = "\n{\n\"" + str(curUser) + "\": {" + template + "\n"+ str(filedata[2:])
            historyEntry = "\n{\n\"" + str(curUser) + "\": {" + template + "\n"+ str(filedata[2:])
        else:
            del history[curUser]
            historyEntry = str(filedata)
            # historyEntry is the object to update
        if debug:
            print("userExists: "+str(userExists))
            print("historyEntry-history:"+ historyEntry)
            print("############################")
            print("")

    else:
        # we don't see a history file, so the new user template should be used
        historyEntry = template
        #historyEntry = "{\n\"" + str(curUser) + "\": {" + template + top_record
        #historyEntry = "\n{\"" + str(curUser) + "\": {" + template + str(filedata[2:])
        if debug:
            print("historyEntry no match")
            print("historyEntry set:" + historyEntry)

        history = json.loads(historyEntry)
        if debug:
            print("historyEntry match")

        if debug:
            print("")
            print("history end")
            # print("historyEntry:"+str(historyEntry))
            print("historyEntry end")
            # print(str(filedata[:-1]) + "\n\"" + str(curUser) + "\": {" + template + "}")

        print("str history:"+str(history))
        history = json.loads(historyEntry)
        print("jsonhistory:"+str(history))
        print("history end:")


def initial_roll():
    # initialize dice
    if debug:
        print("running initial_roll sub")

    for die in range(5):
        dice[die][1] = random.randrange(1, 7)
        die += 1

    reducerolls()


def create_history_record():
    if debug:
        print("")
        print("we're adding a user")


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

    if action == "keep" or action == "drop":
        dicechange()
        score_roll()

    elif action == "roll":
        if debug:
            print("")
            print("rollsleft-roll: " + str(rollsleft))

        if rollsleft == 4:
            initial_roll()
            reducerolls()
            score_roll()
        elif rollsleft in [1, 2, 3]:
            user_check_dice()
            reducerolls()
            score_roll()
            print("")
            print("Rolls remaining: " + str(rollsleft))

    elif action == "status":
        if debug:
            print("rollsleft:" + str(rollsleft))

        if rollsleft in [1, 2, 3]:
            score_roll()
            remaining = rollsleft
        elif rollsleft == 4:
            print("You haven't rolled yet.\n")
            remaining = rollsleft - 1

        print("Rolls remaining: " + str(remaining))

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

    # write current history
    if debug:
        print("write call")

    writehistory()

    if debug:
        print("write done")


def writehistory():
    # not sure if this prints dice or history or both
    # this should just be adding/updating a key in a dict
    # but cant remember how this works anymore

    # dice[] has all updated status for only this user
    # filedata has the data from the file
    # history has filedata in json?

    global dice
    global curUser
    global history
    global filedata
    global historyFile
    global historyEntry

    if debug:
        print("write history")

    for thing in history.keys():
        if curUser == thing:
            # history has curUser already
            if debug:
                print("")
                print("curUser found:" + str(key))
    # TODO: update history[] from dice[]

    if debug:
        print("")
        print("historyFile:" + historyFile)
        print("history:" + str(history))
        print("curUser:" + curUser)
        print("curUser data:" + filedata)

    historyEntry = "{\"" + str(curUser) + "\": {" + template + str(filedata)
    # historyEntry = "{\"" + str(curUser) + "\": {" + template + str(filedata)

    if debug:
        print("")
        print("historyFile:" + historyFile)
        print("history:" + str(history))
        print("curUser:" + curUser)
        print("curUser data:" + filedata)

    exit()

    # write new history file
    file = open(historyFile, "w")
    file.write(str(historyEntry))
    file.close()


def dicechange():
    if debug:
        print("")
        print("argument count:" + str(len(args)))
    if action == "keep" or action == 'drop':
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
                if action == "keep":
                    dice[(int(y) - 1)][0] = heldValues[1]
                elif action == "drop":
                    dice[(int(y) - 1)][0] = heldValues[0]
                else:
                    print("didn't match keep/drop")
                if debug:
                    print("")
                    print("hold value2: " + str(dice[int(y) - 1]))
                    print("hold: " + str(dice[int(y)][0]))
                    print("value: " + str(dice[int(y)][1]))
                    print("dice all2: " + str(dice))


def writehistory():
    # not sure if this prints dice or history or both
    # this should just be adding/updating a key in a dict
    # but cant remember how this works anymore
    if debug:
        print("write history")

    global filedata
    global dice
    global historyEntry

    # TODO: not updating existing records
    # cannot get the json object to update correctly
    historyEntry = "{\"" + str(curUser) + "\": {" + template + str(filedata)
    # historyEntry = "{\"" + str(curUser) + "\": {" + template + str(filedata)

    if debug:
        print("")
        print("historyFile:"+historyFile)
        print("history:"+str(history))
        print("filedata:"+filedata)
        print("curUsername:"+curUser)

        # TODO: dicefield does not exist, what am i looking for
        # print("dicefield:"+[str(diceField)])
        # diceValue = history[str(curUser)]["current"][str(diceField)]

        # print("diceval:"+curUser+" "+diceValue)
        # print("curUser:"+historyEntry["curUser"])


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
        print("running reducerolls")
        print("rollsleft-reduce=" + str(rollsleft))

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
    # only run this when rollsLeft == 0
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
