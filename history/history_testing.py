import random
from history import History

history = History()
if history.does_username_exist('pear') == False:
    history.create_username('pear')

#True - creates a new username
history = History()
username = random.randint(10000, 60000)
history.create_username(username)
history.save_file()
print(history.does_username_exist(username))

#[1,2,3,4,5] - sets dice to [1,2,3,4,5] and writes to file
history = History()
history.data['pear']['current']['dice'] = [1,2,3,4,5]
history.save_file()
print(history.data['pear']['current']['dice'])

#Get top values
history = History()
print(history.get_top())
