# Class for Satellite Categories
'''
ECE 5725 Final Project
Authors: Pavel Berezovsky (pvb23), Haritha Muralidharan (hm535)
Stage 1: Obtaining Coordinates of Interest
Stage 3: Displaying Satellite Information on the PiTFT

SAT CATEGORY CLASS
'''

class Sat_Categories:
	def __init__(self):
        ''' This class is used to store the function/types of satellites
        into each category for filtering '''

		self.weather_list = ['Weather','Earth Resource','Spire','GOES',
							'Search and Rescue','Planet','ARGOS']

		self.communication_list = ['Geostationary','IntelSat','Iridium',
							'Gorizont','Raduga','Molniya','Orbcom',
							'SES','Amateur','Iridium-NEXT','GlobalStar',
							'Experimental Communication','Other Communication']

		self.navigation_list = ['GPS Navigation','GLONASS Navigation',
								'Galileo','Beidou','SBAS','NNSS',
								'Russian LEO']

		self.scientific_list = ['Science','Geodetic','Engineering',
								'Education']

		self.miscellaneous_list = ['Cube Satellites','Disaster Monitoring',
						'Military','Radar','Other','null']
