import random
from history import History

#True - if pear exists
history = History()
print(history.does_username_exist('pear'))

#True - creates a new username
history = History()
username = random.randint(10000, 60000)
history.create_username(username)
history.save_file()
print(history.does_username_exist(username))

#True - creates a new username
history = History()
history.data["pear"]["current"]["dice"] = [1,2,3,4,5]
history.save_file()
print(history.data["pear"])

#Get top values
history = History()
print(history.get_top())
