'''
ECE 5725 Final Project
Authors: Pavel Berezovsky (pvb23), Haritha Muralidharan (hm535)
Stage 1: Obtaining Coordinates of Interest
Stage 3: Displaying Satellite Information on the PiTFT
'''

import os
import subprocess
import pygame
from pygame.locals import *
import time
from display_class import Display
from category_class import Sat_Categories
from sat_info_class import Sat_Info

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') #
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

# initialize pygame and set mouse variable to hide cursor
pygame.init()
pygame.mouse.set_visible(False)

def fifo_set(Flag,final_long,final_lat):
    ''' The function fifo_set has 3 input parameters:
        Flag signifies if message is coordinates (Flag = True) or message is 'Quit' (Flag = False)
        final_long is the longitude coordinate of user choice
        final_lat is the latitude coordinate of user choice

        The purpose of the function is to send the information through 2 FIFO
        to Stage 2 & 4
    '''
	PATH1 = '/home/pi/project/stage1_3/stage2_fifo' # path of 1st FIFO
    if(Flag): # Send coordiantes
		print('The coordinates are: ('+str(final_long)+','+str(final_lat)+')')
		info = str(final_long)+','+str(final_lat)
	elif(not(Flag)): # Send Quit
		print('PROGRAM END')
		info = str('Quit')
	pipe = os.open(PATH1, os.O_WRONLY | os.O_NONBLOCK);
	try: os.write(pipe, info)
	except OSError as err:
		if err.rrno == 6:
			pass
		else:
			raise err
	os.close(pipe)

	PATH2 = '/home/pi/project/stage1_3/stage4_fifo' # path of 2nd FIFO
	if(Flag): # Send coordinates
		print('The coordinates are: ('+str(final_long)+','+str(final_lat)+')')
		info = str(final_long)+','+str(final_lat)
	elif(not(Flag)): # Send Quit
		print('PROGRAM END')
		info = str('Quit')
	pipe2 = os.open(PATH2, os.O_WRONLY | os.O_NONBLOCK);
	try: os.write(pipe2, info)
	except OSError as err:
		if err.rrno == 6:
			pass
		else:
			raise err
	os.close(pipe2)


disp = Display() # Initialize Class Constructor
disp.lvl_1_disp() # Display menu
category = Sat_Categories()  # Initilizing Class Constructor

# Declare initial coordinates of Philips Hall Ithaca if user decides to press enter first
final_lat = 42.443897
final_long = 76.48216

Quit_Flag = False # flag to end infinite while loop

c_flag = -1 # flag to distinguish between lat and long: 1 for lat, 3 for long, -1 initial
Menu_lvl = 1 # Initial level of menu is 1

Type_sat = [] # List of satellites in specific category
Final_sat = [] # Final satellite for level 4 menu

lvl3_first = True # Flag to prevent level 3 display from unnecessary updates
lvl4_first = True # Flag to prevent level 4 display from unnecessary updates

# path of the local satellite file
path = "/home/pi/project/stage2"
readfilename = path + '/local_satellites.txt'

while True:
	# if user pressed the quit button, end while loop
	if(Quit_Flag):
		break;
	x = y = -1 # initial position of user touch on touch screen
	if(Menu_lvl == 1):
		# for mouse press events
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP): # if the event in queue is screen touch
				pos = pygame.mouse.get_pos() # obtain position of touch
				x,y = pos
				if(x > 0 and x < 64 and y > 200):
					# Quit Key
					Quit_Flag = True
					fifo_set(False,final_long,final_lat)
				elif(x > 256 and x < 320 and y > 200):
					# Enter Key
					if(c_flag != -1 and not(disp.get_error())):
						# If new coordinates entered get coordinates and exit while loop
						final_lat = disp.get_lat()
						final_long = disp.get_long()
						fifo_set(True,final_long,final_lat)
						Menu_lvl = 2
					elif(c_flag == -1):
						# If no new coordinates were entered send the initial coordinates
						fifo_set(True,final_long,final_lat)
						Menu_lvl = 2
				elif(x >50 and x <130 and y > 30 and y <70):
					# Latitude Key
					c_flag = 1
				elif(x >50 and x <144 and y > 70 and y <110):
					# Longitude Key
					c_flag = 3
				elif(c_flag != -1):
					# if key is pressed update coordinates
					disp.update_coord(c_flag,x,y)
					disp.lvl_1_disp()
	elif(Menu_lvl == 2):
		disp.lvl_2_count_reset() # reset the number of satellites in each category
		Sat_list = [] # clear Satellite List
        # Read satellite information line by line from text file
		file_object = open(readfilename, 'r')
		ifile = iter(file_object)
		for item in ifile:
			item = list(item.split(","))
			Sat_list.append(Sat_Info(item)) # Initilize satellite object and save in list
        # Parse satellite objects to update category information as well as # of satellites in that category
        for i in range(0,len(Sat_list)):
			Sat_list[i].sat_parsing(category,disp)
		disp.lvl_2_disp() # Display menu
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP): # if the event in queue is screen touch
				pos = pygame.mouse.get_pos() # obtain position of touch
				x,y = pos
				if(x > 28 and x < 135 and y > 57 and y <222):
                    # If category is pressed
					Type_sat = []
                    # Obtain list of satellites in the category chosen by user
					Type_sat = disp.lvl_2_parsing(Sat_list,x,y)
					if(Type_sat is not None):
						lvl3_first = True
						Menu_lvl = 3
				if(x > 200 and x < 300 and y > 200 and y <240):
                    # If back button is pressed go back to level 1 menu
					Menu_lvl = 1
					final_lat = 42.443897
					final_long = 76.48216
					disp.coords[1] = ''
					disp.coords[3] = ''
					disp.lvl_1_disp()
					c_flag = -1
	elif(Menu_lvl == 3):
		if(lvl3_first): # If first time in lvl3 menu update display to level 3
			disp.lvl_3_disp(Type_sat)
			lvl3_first = False
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP): # if the event in queue is screen touch
				pos = pygame.mouse.get_pos() # obtain position of touch
				x,y = pos
				if(x > 180 and x < 220 and y > 200 and y <240):
                    # If back button go back to level 2
					Menu_lvl = 2
				elif(x > 28 and x < 132 and y > 57 and y <57+min(len(Type_sat),5)*33):
                    # IF a satellite name is pressed get satellite  and move to level 4 menu
					Final_sat = []
					Final_sat = disp.lvl_3_parsing(Type_sat,x,y)
					lvl4_first = True
					Menu_lvl = 4
	elif(Menu_lvl == 4):
		if(lvl4_first): # If first time in lvl 4 menu update display to level 4
			disp.lvl_4_disp(Final_sat)
			lvl4_first = False
		for event in pygame.event.get():
			if(event.type is MOUSEBUTTONUP): # if the event in queue is screen touch
				pos = pygame.mouse.get_pos() # obtain position of touch
				x,y = pos
				if(x > 180 and x < 220 and y > 200 and y <240):
                    # If back button is pressed return to level 3 menu
					lvl3_first = True
					Menu_lvl = 3
