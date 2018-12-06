'''
ECE 5725 Final Project
Authors: Pavel Berezovsky (pvb23), Haritha Muralidharan (hm535)
Stage 1: Obtaining Coordinates of Interest
Stage 3: Displaying Satellite Information on the PiTFT

SAT INFO CLASS
'''
import pygame
from pygame.locals import *

# Class to record and parse information from each satellite
class Sat_Info:
    # Each satellite in the local satellite txt file is an object of this class
	def __init__(self,item):
        ''' The initilization of the class has one paramter 'item' which is the
        satellite information as read from the txt file'''

        self.name = str(item[0][2:len(item[0])-1]) # Satellite name
		self.ID= str(item[1][2:len(item[1])-1]) # Satellite unique ID
		self.typ = str(item[2][2:len(item[2])-1]) # Satellite function/type
		self.year = str(item[3][2:len(item[3])-1]) # Satellite year launched
		temp = str(item[4][2:len(item[4])-1])
		self.launch_num = str(filter(str.isdigit, temp)) # Satellite launch #
		self.longitude = str(item[5].strip()) # Satellite Longitude
		self.latitude = str(item[6].strip()) # Satellite latitude
		altitude = str(item[7][:len(item[7])-2])
		self.altitude = altitude.strip() # Satellite altitude
		temp = item[10].find(']')
        # Satellite Color (R,G,B)
		self.color = ((int(item[8][2:])),(int(item[9].strip())),(int(item[10][:temp])))
		self.cat = '' # Satellite Category initialization

	def sat_parsing(self,category,disp):
        ''' The function sat_parsing has to input parameters:
            category is an object of category_class
            disp is an object of display_class

            The purpose of the function is to uptate the satellite category and
            update the number of satellites in that category
        '''
		for Type in category.weather_list:
			if(self.typ == Type): # If satellite funtion/type is in the category
                # Increase the # of satellites in that category by 1
				disp.lvl_2_count[0] = str(int(disp.lvl_2_count[0])+1)
				self.cat = 'Weather' # Update the category of the satellite
				return

		for Type in category.communication_list:
			if(self.typ == Type):
				disp.lvl_2_count[2] = str(int(disp.lvl_2_count[2])+1)
				self.cat = 'Communication'
				return

		for Type in category.navigation_list:
			if(self.typ == Type):
				disp.lvl_2_count[4] = str(int(disp.lvl_2_count[4])+1)
				self.cat = 'Navigation'
				return

		for Type in category.scientific_list:
			if(self.typ == Type):
				disp.lvl_2_count[6] = str(int(disp.lvl_2_count[6])+1)
				self.cat = 'Scientific'
				return

		for Type in category.miscellaneous_list:
			if(self.typ == Type):
				disp.lvl_2_count[8] = str(int(disp.lvl_2_count[8])+1)
				self.cat = 'Miscellaneous'
				return
