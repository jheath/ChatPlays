import random
from history import History
from history_highscore import HistoryHighscore

username_to_test = 'Pear'
score = 90

history = History()
if history.does_username_exist(username_to_test) == False:
    history.create_username(username_to_test)


# Test daily entry creation
history_highscore = HistoryHighscore(history)
history_highscore.submit_score(username_to_test, score)
