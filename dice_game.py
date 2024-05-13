import sys
import random

# var inits
heldText = "Held"
notHeldText = "Not Held"
dice[:5] = 0
diceHeld[:5] = notHeldText

rollsLeft = 3
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
        elif val == range(1:6):
            if diceHeld[int(val) - 1] == notHeldText:
                diceHeld[int(val) - 1] = heldValue


def reroll():
    for x in range(5):
        if diceHeld[x] == notHeldText:
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
        diceHeld[x] = notHeldText


def score_roll():
    score = 0
    num[:6] = 0
    for x in range(5):
        print('Dice #' + str(x + 1) + ': ' + str(dice[x]))

    # check for straights
    # looks right, range may be wrong -erg
    count = 0
    for x in range(1:5):
        if dice[num[x]] > dice[num[x -1]]
            count += 1
        else
            count = 0
        # initial score
        score += dice[x]

    # small straight
    if count >= 2:
        score = 30
    # Large straight
    elif count > 3:
        score = 40
    # Yahtzee
    elif count > 4:
        score = 50


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
