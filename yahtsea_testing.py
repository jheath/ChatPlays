import sys
import random
import os.path
import json
from yahtsea import YahtSea

args = sys.argv
username = args[1]
action = args[2]
targets = []
if len(args) > 3:
    targets = args[3]

yahtsea = YahtSea(username)

if action == 'get_active_game_users':
	print(yahtsea.get_active_game_users())

if action == 'play':
    print(yahtsea.play())

if action == 'hold':
    if targets:
        target_pieces = targets.split(',')
        target_pieces_as_int = [int(target.strip()) for target in target_pieces if target.strip().isdigit()]
    else:
        target_pieces_as_int = []
    print(yahtsea.hold(target_pieces_as_int))

if action == 'roll':
    print(yahtsea.roll())

if action == 'leaderboard':
    print(yahtsea.leaderboard())

if action == 'end_round':
    print(yahtsea.end_round())

if action == 'resume':
    print(yahtsea.resume())
