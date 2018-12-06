'''
ECE 5725 Final Project
Authors: Pavel Berezovsky (pvb23), Haritha Muralidharan (hm535)
Stage 1: Obtaining Coordinates of Interest
Stage 3: Displaying Satellite Information on the PiTFT

DISPLAY CLASS
'''

import pygame
from pygame.locals import *

# Class to display stage 1 & 3 on PiTFT
class Display:
	# Constructor
	def __init__(self):
		# define Black, White, Red, Green RGB colors
		self.Color = ((255,255,255),(0,0,0),(255,0,0),(0,255,0))
		# Set screen to correct pixel dimensions of PiTFT
		self.screen = pygame.display.set_mode((320, 240))
		# Load satellite background image
		self.sat_background= pygame.image.load("/home/pi/python_games/Sat_back.png")
		# Create a rectangle around background
		self.sat_rect = self.sat_background.get_rect()
		# Creating font of two sizes
		self.my_font = [pygame.font.Font(None, 23),pygame.font.Font(None, 20)]


		# Define name and position of error in coordinates; 1st lat, 2nd long
		self.coord_error = ["!!!",(20,50),"!!!",(20,90)]
		# Define initial coordinate position and value; 1st lat, 2nd long
		self.coords = [(180,50),'',(180,90),'']
		# Error Flags for error in coordinates
		self.long_error = False
		self.lat_error = False

		# Define the button position and name for lvl 1
		self.lvl_1_buttons = { "WHAT'S FLYING OVER YOU?":(160,20),
			'Latitude: ':(93,50),'Longitude: ':(100,90),
			'1':(32,140),'2':(96,140),'3':(160,140),'4':(224,140),'5':(288,140),
			'6':(32,180),'7':(96,180),'8':(160,180),'9':(224,180),'0':(288,180),
			'Quit':(32, 220),'.':(96,220),'-':(160,220),
            '<--':(224,220),'Enter':(288, 220)}

		# Text displayed in lvl 2
		self.lvl_2_text = {"WHAT'S FLYING OVER YOU?":(160,20),
			'Satellite Categories:':(80,40),
			'# Overhead:':(270,40)}

		# Button coordinates for lvl 2 & 3
		self.button_coord = ((30 ,73.5),(30,106.5),(30,139.5),(30,172.5),(30,205.5),(200, 220))

		# Define the button position and name for lvl 2
		self.lvl_2_buttons = {'Weather':self.button_coord[0],
			'Communication':self.button_coord[1],
			'Navigation':self.button_coord[2],
			'Scientific':self.button_coord[3],
			'Miscellaneous':self.button_coord[4],
			'New Coordinates':self.button_coord[5]}

		# Define sat count in each category for lvl 2
		self.lvl_2_count = ['0',(270 ,73.5),
			'0',(270,106.5),
			'0',(270,139.5),
			'0',(270,172.5),
			'0',(270,205.5)]

		# Define text for lvl 3
		self.lvl_3_text = {"WHAT'S FLYING OVER YOU?":(160,20),
			'Satellite Overhead:':(80,40),'Back':self.button_coord[5]}

		# Define text for lvl 4
		self.lvl_4_text_1 = {"WHAT'S FLYING OVER YOU?":(160,20),
			'Satellite Information:':(80,40)}

		self.lvl_4_text_2 = {'Name:':(50,60),
			 'ID #:':(50,80),'Type:':(50,100),'Year:':(50,120),
			 'Launch #':(50,140),'Longitude:':(50,160),
			 'Latitude:':(50,180),'Altitude:':(50,200),'Back':(200,220)}


	def lvl_1_draw_rect(self):
        ''' Function lvl_1_draw_rect has no input parameters.
            The purpose of the function is to draw rectangles around each button
            to indicate bounds for lvl 1
        '''
		pygame.draw.rect(self.screen, self.Color[0], (0,120,64,40), 1) # rect around '1'
		pygame.draw.rect(self.screen, self.Color[0], (64,120,64,40), 1) # rect around '2'
		pygame.draw.rect(self.screen, self.Color[0], (128,120,64,40), 1) # rect around '3'
		pygame.draw.rect(self.screen, self.Color[0], (192,120,64,40), 1) # rect around '4'
		pygame.draw.rect(self.screen, self.Color[0], (256,120,64,40), 1) # rect around '5'
		pygame.draw.rect(self.screen, self.Color[0], (0,160,64,40), 1) # rect around '6'
		pygame.draw.rect(self.screen, self.Color[0], (64,160,64,40), 1) # rect around '7'
		pygame.draw.rect(self.screen, self.Color[0], (128,160,64,40), 1) # rect around '8'
		pygame.draw.rect(self.screen, self.Color[0], (192,160,64,40), 1) # rect around '9'
		pygame.draw.rect(self.screen, self.Color[0], (256,160,64,40), 1) # rect around '0'
		pygame.draw.rect(self.screen, self.Color[0], (0,200,64,40), 1) # rect around 'Quit'
		pygame.draw.rect(self.screen, self.Color[0], (64,200,64,40), 1) # rect around '.'
		pygame.draw.rect(self.screen, self.Color[0], (128,200,64,40), 1) # rect around '-'
		pygame.draw.rect(self.screen, self.Color[0], (192,200,64,40), 1) # rect around 'BS'
		pygame.draw.rect(self.screen, self.Color[0], (256,200,64,40), 1) # rect around 'Enter'


	def lvl_2_draw_rect(self):
        ''' Function lvl_2_draw_rect has no input parameters.
            The purpose of the function is to draw rectangles around each
            button to indicate bounds for lvl 2.
        '''
		pygame.draw.rect(self.screen, self.Color[0], (28,57,105,33), 1) # rect around 'Weather'
		pygame.draw.rect(self.screen, self.Color[0], (28,90,105,33), 1) # rect around 'Communication'
		pygame.draw.rect(self.screen, self.Color[0], (28,123,105,33), 1) # rect around 'Navigation'
		pygame.draw.rect(self.screen, self.Color[0], (28,156,105,33), 1) # rect around 'Scientific'
		pygame.draw.rect(self.screen, self.Color[0], (28,189,105,33), 1) # rect around 'Miscellaneous'


	def lat_bounds_check(self):
        '''	Function lat_bounds_check has no input parameters.
            The purpose of the function is to check if lat coord is out of bounds.
        '''
		if(self.coords[1]):
			try: # If  lat coords is a float
				temp_val = abs(float(self.coords[1]))
				# Lat bounds are: -90<= lat <= 90
				if(90-temp_val <0):
					self.lat_error = True
				else:
					self.lat_error = False
			except ValueError: # if coord is not a float
				self.lat_error = True


	def long_bounds_check(self):
        '''	Function long_bounds_check has no input parameters.
            The purpose of the function is to check if long coord is out of bounds.
        '''
		if(self.coords[3]):
			try:# If long coord is a float
				temp_val = abs(float(self.coords[3]))
				# Lat bounds are: -180<= lat <= 180
				if(180-temp_val <0):
					self.long_error = True
				else:
					self.long_error = False
			except ValueError: # if coord is not a float
				self.long_error = True


	def coordinate_add(self,coordinate,c_flag):
        '''	Function coordinate_add has 2 parametrs:
            coordinate is a digit value that user input
            c_flag is a flag 1 or 3 where 1 for lat and 3 for long

            The purpose fo the function is to add a new value to
            lat or long coordinate.
        '''
		self.coords[c_flag] += str(coordinate)
		# checking bounds
		if(c_flag == 1):
			self.lat_bounds_check()
		elif(c_flag == 3):
			self.long_bounds_check()


	def coordinate_rm(self,c_flag):
        ''' The function coordinate_rm has 1 input parameter:
            c_flag is a flag 1 or 3 where 1 for lat and 3 for long

            The purpose of the function is to remove the last digit from
            lat or long coordinate.
            '''
		# Removing last value
		coordinate = self.coords[c_flag]
		coordinate = coordinate[:-1]
		self.coords[c_flag] = coordinate
		# cheking bounds
		if(c_flag == 1):
			self.lat_bounds_check()
		elif(c_flag == 3):
			self.long_bounds_check()


	def get_error(self):
        '''	The function get_error has no input parameters.
            The purpose of the function is to return a bool Tru if error exist
            in any coordinate.
        '''
		if(self.lat_error or self.long_error):
			return True
		else:
			return False


	def get_lat(self):
        '''	The function get_lat has no input parameters.
            The purpose of the function is to return the value of latitude.
        '''
		return self.coords[1]


	# Function returns the value of longitude
	def get_long(self):
        '''	The function get_long has no input parameters.
            The purpose of the function is to return the value of longitude.
        '''
		return self.coords[3]


	def update_coord(self,c_flag,x,y):
        ''' The function update_coord has 3 parameters:
            c_flag is a flag 1 or 3 where 1 for lat and 3 for long
            x is the location of user touch on touchscreen with respect to x-axis
            y is the location of user touch on touchscreen with respect to y-axis

            The purpose of the function is to perform call helper functions to
            add or remove digits in the latitude and longitude coordiantes based
            on user presses on the touchscreen
        '''
		if(y > 120 and y < 160):
			if(x > 0 and x < 64):
				# 1 Key
				self.coordinate_add(1,c_flag)
			elif(x > 64 and x < 128):
				# 2 Key
				self.coordinate_add(2,c_flag)
			elif(x > 128 and x < 192):
				# 3 Key
				self.coordinate_add(3,c_flag)
			elif(x > 192 and x < 256):
				# 4 Key
				self.coordinate_add(4,c_flag)
			elif(x > 256 and x < 320):
				# 5 Key
				self.coordinate_add(5,c_flag)
		elif(y > 160 and y < 200):
			if(x > 0 and x < 64):
				# 6 Key
				self.coordinate_add(6,c_flag)
			elif(x > 64 and x < 128):
				# 7 Key
				self.coordinate_add(7,c_flag)
			elif(x > 128 and x < 192):
				# 8 Key
				self.coordinate_add(8,c_flag)
			elif(x > 192 and x < 256):
				# 9 Key
				self.coordinate_add(9,c_flag)
			elif(x > 256 and x < 320):
				# 0 Key
				self.coordinate_add(0,c_flag)
		elif(y > 200):
			if(x > 64 and x < 128):
				# '.' Key
				self.coordinate_add('.',c_flag)
			elif(x > 128 and x < 192):
				# '-' Key
				self.coordinate_add('-',c_flag)
			elif(x > 192 and x < 256):
				# Backspace Key
				self.coordinate_rm(c_flag)


	def lvl_2_count_reset(self):
        ''' The function lvl_2_count_reset has no input parameters.
            The purpose of the function is to reset the number of satellites in
            each category to 0 for every new reading of the local satellite
            txt file.
        '''
        self.lvl_2_count[0] ='0'
		self.lvl_2_count[2] ='0'
		self.lvl_2_count[4] ='0'
		self.lvl_2_count[6] ='0'
		self.lvl_2_count[8] ='0'


	def lvl_2_new_sat_list(self,Sat_list,Typ):
        ''' The function lvl_2_new_sat_list has 2 input parameters:
            Sat_list is a list of obects of sat_info_class
            Typ is a satellite category_class

            The purpose of this function is to return a list of all satellite
            objects in the specific category
        '''
		New_sat_list = [] # new list
		for sat in Sat_list:
			if(sat.cat == Typ): # if satellite function/type matches the sat type
				New_sat_list.append(sat) # add satellite object to new list
		return New_sat_list


	def lvl_2_parsing(self,Sat_list,x,y):
        ''' The function lvl_2_parsing has 3 input parameters:
            Sat_list is a list of objects of sat_info_class
            x is the location of user touch on touchscreen with respect to x-axis
            y is the location of user touch on touchscreen with respect to y-axis

            The purpose of this function is to return a list of all satellite
            objects in the specific category
        '''
        if(y > 57 and y < 90):
			return self.lvl_2_new_sat_list(Sat_list,'Weather')
		elif(y > 90 and y < 123):
			return self.lvl_2_new_sat_list(Sat_list,'Communication')
		elif(y > 123 and y < 156):
			return self.lvl_2_new_sat_list(Sat_list,'Navigation')
		elif(y > 156 and y < 189):
			return self.lvl_2_new_sat_list(Sat_list,'Scientific')
		elif(y > 189 and y < 222):
			return self.lvl_2_new_sat_list(Sat_list,'Miscellaneous')

	# Parsing lvl 3 to return the satellite in the touch area pressed
	def lvl_3_parsing(self,Type_sat,x,y):
        ''' The function lvl_3_parsing has 3 input parameters
            Type_sat is a list of objects in a satellite category
            x is the location of user touch on touchscreen with respect to x-axis
            y is the location of user touch on touchscreen with respect to y-axis

            The purpose of this function is to return the name of the satellite
            chosen by user
        '''
		for i in range(0,min(len(Type_sat),5)):
			if(y > 57+(i*33) and y < 57+((i+1)*33)):
				return Type_sat[i]

	def lvl_1_disp(self):
        ''' The function lvl_1_disp has no input parameters.
            The purpose of the function to update display on PiTFT for lvl 1 menu
        '''
        self.screen.fill(self.Color[1]) # Erase the workspace
		self.screen.blit(self.sat_background,self.sat_rect) # Add background
		self.lvl_1_draw_rect() # Draw all the rectangles
		# Display text of all buttons on PiTFT screen
		for my_text, text_pos in self.lvl_1_buttons.items():
			text_surface = self.my_font[0].render(my_text, True, self.Color[0])
			rect = text_surface.get_rect(center=text_pos)
			self.screen.blit(text_surface, rect)
		# Display Latitude value
		text_surface = self.my_font[0].render(self.coords[1], True, self.Color[0])
		rect = text_surface.get_rect(center=self.coords[0])
		self.screen.blit(text_surface, rect)
		# Display Longitude value
		text_surface = self.my_font[0].render(self.coords[3], True, self.Color[0])
		rect = text_surface.get_rect(center=self.coords[2])
		self.screen.blit(text_surface, rect)

		if(self.lat_error): # if there is a latitude error display: !!!
			text_surface = self.my_font[0].render(self.coord_error[0], True, self.Color[2])
			rect = text_surface.get_rect(center=self.coord_error[1])
			self.screen.blit(text_surface, rect)

		if(self.long_error): # if there is a longitude error display: !!!
			text_surface = self.my_font[0].render(self.coord_error[2], True, self.Color[2])
			rect = text_surface.get_rect(center=self.coord_error[3])
			self.screen.blit(text_surface, rect)
		pygame.display.flip() # Update screen


	def lvl_2_disp(self):
        ''' The function lvl_2_disp has no input parameters.
            The purpose of the function to update display on PiTFT for lvl 2 menu
        '''
		self.screen.fill(self.Color[1]) # Erase the workspace
		self.screen.blit(self.sat_background,self.sat_rect) # Add background
		self.lvl_2_draw_rect() # Draw all the rectangles
		for my_text, text_pos in self.lvl_2_text.items():
			text_surface = self.my_font[0].render(my_text, True, self.Color[0])
			rect = text_surface.get_rect(center=text_pos)
			self.screen.blit(text_surface, rect)
		# Display text of all buttons on PiTFT screen
		for my_text, text_pos in self.lvl_2_buttons.items():
			text_surface = self.my_font[1].render(my_text, True, self.Color[0])
			rect = text_surface.get_rect(midleft=text_pos)
			self.screen.blit(text_surface, rect)
        # Display the # of satellites in each category
		for i in range(0,len(self.lvl_2_count),2):
			text_surface = self.my_font[1].render(self.lvl_2_count[i], True, self.Color[3])
			rect = text_surface.get_rect(center=self.lvl_2_count[i+1])
			self.screen.blit(text_surface, rect)
		pygame.display.flip() # Update screen


	# Function to update display on PiTFT for lvl 3 menu
	def lvl_3_disp(self,Typ_sat):
        ''' The function lvl_3_disp has 1 input parameter:
            Typ_sat is a list of satellited objects in one category

            The purpose of the function to update display on PiTFT for lvl 3 menu
        '''
		self.screen.fill(self.Color[1]) # Erase the workspace
		self.screen.blit(self.sat_background,self.sat_rect) # Add background
		for my_text, text_pos in self.lvl_3_text.items():
			text_surface = self.my_font[0].render(my_text, True, self.Color[0])
			rect = text_surface.get_rect(center=text_pos)
			self.screen.blit(text_surface, rect)
        # Make Satellite names display as buttons on the PiTFT
		Sat_name = {}
		for i in range(0,min(len(Typ_sat),5)):
			Sat_name[Typ_sat[i].name] = self.button_coord[i]
			pygame.draw.rect(self.screen, self.Color[0], (28,57+(i*33),132,33), 1)
		c_c = 0
        # Display Satellite names in specific color
		for my_text, text_pos in Sat_name.items():
			text_surface = self.my_font[1].render(my_text, True, Typ_sat[c_c].color)
			rect = text_surface.get_rect(midleft=text_pos)
			self.screen.blit(text_surface, rect)
			c_c += 1
		pygame.display.flip() # Update screen


	def lvl_4_disp(self,Final_sat):
        ''' The function lvl_4_disp has 1 input parameter:
            Final_sat is a satellite object of sat_info_class

            The purpose of the function to update display on PiTFT for lvl 4 menu
        '''
		self.screen.fill(self.Color[1]) # Erase the workspace
		self.screen.blit(self.sat_background,self.sat_rect) # Add background
        # Display Title
		for my_text, text_pos in self.lvl_4_text_1.items():
			text_surface = self.my_font[0].render(my_text, True, self.Color[0])
			rect = text_surface.get_rect(center=text_pos)
			self.screen.blit(text_surface, rect)
        # Display Satellite info name
		for my_text, text_pos in self.lvl_4_text_2.items():
			text_surface = self.my_font[1].render(my_text, True, self.Color[0])
			rect = text_surface.get_rect(midleft=text_pos)
			self.screen.blit(text_surface, rect)
        # Display Satellite information
		Sat_info = {str(Final_sat.name):(140,60),str(Final_sat.ID):(140,80),
			str(Final_sat.typ):(140,100),str(Final_sat.year):(140,120),
			str(Final_sat.launch_num):(140,140),str(Final_sat.longitude):(140,160),
			str(Final_sat.latitude):(140,180),str(Final_sat.altitude):(140,200)}
        # Display back button
		for my_text, text_pos in Sat_info.items():
			text_surface = self.my_font[1].render(my_text, True, self.Color[3])
			rect = text_surface.get_rect(midleft=text_pos)
			self.screen.blit(text_surface, rect)
		pygame.display.flip() # Update screen
