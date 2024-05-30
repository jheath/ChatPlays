import sys
import random
import os.path
import json
from yahtsea import YahtSea

args = sys.argv
username = args[1]
action = args[2]
if len(args) > 3:
    targets = args[3]

yahtsea = YahtSea(username)

if action == 'get_active_game_username':
	print(yahtsea.get_active_game_username())

if action == 'play':
    print(yahtsea.play())

if action == 'hold':
    target_pieces = targets.split(',')
    target_pieces_as_int = [int(target.strip()) for target in target_pieces]
    print(yahtsea.hold(target_pieces_as_int))

if action == 'roll':
    print(yahtsea.roll())

if action == 'status':
    print(yahtsea.status())

if action == 'end_round':
    print(yahtsea.end_round())
