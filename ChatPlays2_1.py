import concurrent.futures
import time
import random
import keyboard
import pydirectinput
import pyautogui
import TwitchPlays_Connection
from TwitchPlays_KeyCodes import *

##################### GAME VARIABLES #####################

# Replace this with your Twitch username. Must be all lowercase.
TWITCH_CHANNEL = 'peargamer7857' 

# If streaming on Youtube, set this to False
STREAMING_ON_TWITCH = True

# Replace this with your Youtube's Channel ID
# Find this by clicking your Youtube profile pic -> Settings -> Advanced Settings
YOUTUBE_CHANNEL_ID = 'peargamer7857' 

# If you're using an Unlisted stream to test on Youtube, replace "None" below with your stream's URL in quotes.
# Otherwise you can leave this as "None"
YOUTUBE_STREAM_URL = None

##################### MESSAGE QUEUE VARIABLES #####################

# MESSAGE_RATE controls how fast we process incoming Twitch Chat messages. It's the number of seconds it will take to handle all messages in the queue.
# This is used because Twitch delivers messages in "batches", rather than one at a time. So we process the messages over MESSAGE_RATE duration, rather than processing the entire batch at once.
# A smaller number means we go through the message queue faster, but we will run out of messages faster and activity might "stagnate" while waiting for a new batch. 
# A higher number means we go through the queue slower, and messages are more evenly spread out, but delay from the viewers' perspective is higher.
# You can set this to 0 to disable the queue and handle all messages immediately. However, then the wait before another "batch" of messages is more noticeable.
MESSAGE_RATE = 0.5
# MAX_QUEUE_LENGTH limits the number of commands that will be processed in a given "batch" of messages. 
# e.g. if you get a batch of 50 messages, you can choose to only process the first 10 of them and ignore the others.
# This is helpful for games where too many inputs at once can actually hinder the gameplay.
# Setting to ~50 is good for total chaos, ~5-10 is good for 2D platformers
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100 # Maximum number of threads you can process at a time 

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []
pyautogui.FAILSAFE = False

##########################################################
def loop_number(string):
    letter, number = string.split(',')
    if abs(int(number)) < 11:
        for i in range(int(number)):
            pydirectinput.press(letter)

def hold_key(string):
	try:

		letter, number,varx = string.split(',')

		if number == "a" :
			number = "r"

		if number == "b" :
			number = "e"

		if number == "up" :
			number = "w"

		if number == "down" :
			number = "s"

		if number == "left" :
			number = "a"

		if number == "right" :
			number = "d"

		if number == "select" :
			number = "q"

		if number == "start" :
			number = "z"

		#if msg == "shoot" :
			#pydirectinput.mouseDown(button="left")
			#time.sleep(1)
			#pydirectinput.mouseUp(button="left")

		print(letter)
		print(number)
		print(float(varx))
		
		if abs(float(varx)) < 10: 
			pydirectinput.keyDown(number)
			time.sleep(abs(float(varx)))
			pydirectinput.keyUp(number)

	except:
		print("caught an error")



  

# Count down before starting, so you have time to load up the game
countdown = 0
while countdown > 0:
	print(countdown)
	countdown -= 1
	time.sleep(1)
if STREAMING_ON_TWITCH:
	t = TwitchPlays_Connection.Twitch()
	t.twitch_connect(TWITCH_CHANNEL)
else:
	t = TwitchPlays_Connection.YouTube()
	t.youtube_connect(YOUTUBE_CHANNEL_ID, YOUTUBE_STREAM_URL)

def handle_message(message):
	try:

		msg = message['message'].lower()
		username = message['username'].lower()
		print("Got this message from " + username + ": " + msg)
		parts = msg.split()
		for part in parts:
			 
			# Now that you have a chat message, this is where you add your game logic.
			# Use the "HoldKey(KEYCODE)" function to permanently press and hold down a key.
			# Use the "ReleaseKey(KEYCODE)" function to release a specific keyboard key.
			# Use the "HoldAndReleaseKey(KEYCODE, SECONDS)" function press down a key for X seconds, then release it.
			# Use the pydirectinput library to press or move the mouse

			# I've added some example videogame loic code below:

			###################################
			# Example GTA V Code
			###################################

			# If the chat message is "left", then hold down the A key for 2 second
			
			if part.startswith("hold,"):
				hold_key(part)
		
##Z2 jumpright			
			if part == "jumpright":
				HoldKey(D)
				time.sleep(.5)
				HoldKey(R)
				time.sleep(.5)
				ReleaseKey(D)
				ReleaseKey(R)
##Z2 jumpleft
			if part == "jumpleft":
				HoldKey(A)
				time.sleep(.5)
				HoldKey(R)
				time.sleep(.5)
				ReleaseKey(A)
				ReleaseKey(R)

			if part == "downstab":
				pydirectinput.press('r')
				HoldKey(S)
				time.sleep(.7)
				HoldKey(E)
				time.sleep(.7)
				ReleaseKey(S)
				ReleaseKey(E)



			if part == "jump":
				pydirectinput.press('r')

			if part == "crouch":
				HoldKey(S)

			if part == "stand":
				ReleaseKey(S)

			if part == "crotch":
				HoldKey(S)

##Z2 reset			

			#if part == "reset":
				#pydirectinput.press('z')
				#HoldKey(P)
				#time.sleep(1)
				#HoldKey(L)
				#time.sleep(1)
				#ReleaseKey(P)
				#ReleaseKey(L)

##crystallis warp function
			#if part == "warp":
				#HoldKey(R)
				#time.sleep(1)
				#HoldKey(E)
				#time.sleep(1)
				#HoldKey(L)
				#time.sleep(1)
				#ReleaseKey(R)
				#ReleaseKey(E)
				#ReleaseKey(L)

			if part == "charge":
				HoldKey(E)
				time.sleep(1.6)
				ReleaseKey(E)

			if part == "dash":
				HoldKey(R)
				time.sleep(4)
				ReleaseKey(R)

##final fantasy map command
			#if part == "map":
				#HoldKey(E)
				#time.sleep(1)
				#HoldKey(Q)
				#time.sleep(1)
				#ReleaseKey(E)
				#ReleaseKey(Q)

			if part == "runright":
				HoldKey(D)
		
			if part == "runleft":
				HoldKey(A)

			if part == "runup":
				HoldKey(W)

			if part == "rundown":
				HoldKey(S)
		
			if part == "stop":
				ReleaseKey(D)
				ReleaseKey(A)
				ReleaseKey(W)
				ReleaseKey(S)
				

			if part.startswith("a,"):
				part = part.replace("a","r")
				part = part.replace("A","r")
				loop_number(part)

			if part.startswith("b,"):
				part = part.replace("b","e")
				part = part.replace("B","e")
				loop_number(part)		

			if "up" == part:
				pydirectinput.press('w')
				
				

			if "down" == part:
				pydirectinput.press('s')
				
				

			if "left" == part:
				pydirectinput.press('a')
				
				

			if "right" == part:
				pydirectinput.press('d')
				
			

			if "a" == part:
				pydirectinput.press('r')
				
			

			if "b" == part:
				pydirectinput.press('e')
			

			if "lb" == part:
				pydirectinput('f')
				

			if "rb" == part:
				pydirectinput('g')
				

			if "select" == part:
				pydirectinput.press('q')
				

			if "start" == part:
				pydirectinput.press('z')

			if "x" == part:
				pydirectinput.press('t')
			

			if "turbo" == part:
				pydirectinput.mouseDown(button="left")
				time.sleep(1)
				pydirectinput.mouseUp(button="left")
				

			if "killthegibson" == part:
				print("good bye")
				exit()
			####################################
			####################################

	except Exception as e:
		print("Encountered exception: " + str(e))


while True:

	active_tasks = [t for t in active_tasks if not t.done()]

	#Check for new messages
	new_messages = t.twitch_receive_messages();
	if new_messages:
		message_queue += new_messages; # New messages are added to the back of the queue
		message_queue = message_queue[-MAX_QUEUE_LENGTH:] # Shorten the queue to only the most recent X messages

	messages_to_handle = []
	if not message_queue:
		# No messages in the queue
		last_time = time.time()
	else:
		# Determine how many messages we should handle now
		r = 1 if MESSAGE_RATE == 0 else (time.time() - last_time) / MESSAGE_RATE
		n = int(r * len(message_queue))
		if n > 0:
			# Pop the messages we want off the front of the queue
			messages_to_handle = message_queue[0:n]
			del message_queue[0:n]
			last_time = time.time();
	# If user presses Shift+Backspace, automatically end the program
	if keyboard.is_pressed('shift+backspace'):
		exit()

	if not messages_to_handle:
		continue
	else:
		for message in messages_to_handle:
			if len(active_tasks) <= MAX_WORKERS:
				active_tasks.append(thread_pool.submit(handle_message, message))
			else:
				print(f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
