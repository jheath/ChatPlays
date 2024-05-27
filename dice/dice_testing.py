import sys
from dice import Dice

#[0,0,0,0,0]
dice = Dice()
print(dice.get_dice_values())

#[0,1,0,1,0]
dice = Dice([0,1,0,1,0])
print(dice.get_dice_values())

#[x,x,x,x,x]
dice = Dice()
dice.roll()
print(dice.get_dice_values())

#[x,1,x,1,x]
dice = Dice([0,1,0,1,0])
dice.roll()
print(dice.get_dice_values())

#['YAHTZEE', 50]
dice = Dice([3,3,3,3,3])
print(dice.get_score())

#['Large Straight', 40]
dice = Dice([5,2,1,4,3])
print(dice.get_score())

#['Large Straight', 40]
dice = Dice([5,2,6,4,3])
print(dice.get_score())

#['Small Straight', 30]
dice = Dice([2,1,1,4,3])
print(dice.get_score())

#['Small Straight', 30]
dice = Dice([5,2,5,4,3])
print(dice.get_score())

#['Full House', 25]
dice = Dice([3,2,3,2,3])
print(dice.get_score())

#['Four of a kind', 12]
dice = Dice([3,3,3,1,3])
print(dice.get_score())

#['Three of a kind', 9]
dice = Dice([3,2,3,1,3])
print(dice.get_score())

#['No points', 0]
dice = Dice([6,6,3,1,3])
print(dice.get_score())
