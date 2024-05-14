import random

# var inits
# dice[number][held value,dice value]
heldValues = ["Not Held", "Held"]
dice = [[heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0],
        [heldValues[0], 0]]

rollsleft = 3


# initialize dice
def initial_roll():
    for die in range(5):
        dice[die][1] = random.randrange(1, 7)
        die += 1
        continue
    reducerolls()


# Game loop
def main_loop():

    playing = True
    while playing:
        if rollsleft == 3:
            initial_roll()
        elif rollsleft > 0:
            user_check_dice()
            reroll()
        else:
            score_roll()
            val = input('Play again?(y or n)\n')
            if val == 'n':
                playing = False
            else:
                resetrolls()
                resethelds()


# Let users hold dice
def user_check_dice():
    userdone = False
    while not userdone:
        for x in range(5):
            print('Dice #' + str(x + 1) + ': ' + str(dice[x][1]) + '   ' + str(dice[x][0]))
        val = input('Type the number of the die to hold it or type C to continue.\n')

        if val == "C" or val == 'c':
            userdone = True
        elif val == "1" or val == "2" or val == "3" or val == "4" or val == "5":
            if dice[int(val) - 1][0] == heldValues[1]:
                dice[int(val) - 1][0] = heldValues[0]
            else:
                dice[int(val) - 1][0] = heldValues[1]


def reroll():
    for x in range(5):
        if dice[x][0] == heldValues[0]:
            dice[x][1] = random.randrange(1, 7)
            continue
    reducerolls()


def reducerolls():
    global rollsleft
    rollsleft -= 1


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
        print('Dice #' + str(x + 1) + ': ' + str(dice[x][1]))

    # check for yahtzee
    if dice[0][1] == dice[1] and dice[1] == dice[2] and dice[2] == dice[3] and dice[3] == dice[4]:
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
            score += dice[x][1]

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

    # 4 of a kind
    # 3 of a kind

    print("")
    if special != "":
        print("** " + special + " **")
    print('Your score = ' + str(score))


main_loop()
