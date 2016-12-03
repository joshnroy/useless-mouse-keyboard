import wiiboard
import pygame
import time
import pyautogui
import threading
pyautogui.FAILSAFE = False

THRESHOLD = 5
MOVEMENT_SCALE = 2

mouse_move_data = None
done = False
click = False
key_sim = None

def avg(x,y):
	return (x+y)/2

def threshold(x):
	return x**2 if abs(x) > THRESHOLD else 0

def move_mouse(tr,br,bl,tl):
	tAvg = avg(tr, tl)
	bAvg = avg(br, bl)
	rAvg = avg(tr, br)
	lAvg = avg(tl, bl)

	mvVert = threshold(bAvg - tAvg) * MOVEMENT_SCALE
	mvHorz = threshold(rAvg - lAvg) * MOVEMENT_SCALE

	pyautogui.moveRel(mvHorz, mvVert, 1)

def mouse_control():
	global mouse_move_data
	global done
	global click
	while(not done):
		if not mouse_move_data is None:
			move_mouse(mouse_move_data.topRight,
					mouse_move_data.bottomRight, 
					mouse_move_data.bottomLeft,
					mouse_move_data.topLeft)
			mouse_move_data = None


def main():
	global mouse_move_data
	global done

	board = wiiboard.Wiiboard()

	pygame.init()
	
	address = board.discover()
	board.connect(address) #The wii board must be in sync mode at this time

	time.sleep(0.1)
	board.setLight(True)

	# make the thread for mouse control
	mouse_thread = threading.Thread(target=mouse_control)
	mouse_thread.start();

	while (not done):
		time.sleep(0.05)
		for event in pygame.event.get():
			if event.type == wiiboard.WIIBOARD_CONNECTED:
				print "The board is active. You know not what you have done."
			elif event.type == wiiboard.WIIBOARD_DISCONNECTED:
				print "You have disconnected the board."
			elif event.type == wiiboard.WIIBOARD_MASS:
				if (event.mass.totalWeight > 5):   #10KG. otherwise you would get alot of useless small events!
					if mouse_move_data is None:
						print "updating mouse_move_data"
						mouse_move_data = event.mass
				#etc for topRight, bottomRight, bottomLeft. buttonPressed and buttonReleased also available but easier to use in seperate event
				
			elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
				print "Button pressed!"

			elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
				print "Button released"
				done = True
			
			#Other event types:
			#wiiboard.WIIBOARD_CONNECTED
			#wiiboard.WIIBOARD_DISCONNECTED

	board.disconnect()
	pygame.quit()

#Run the script if executed
if __name__ == "__main__":
	main()
