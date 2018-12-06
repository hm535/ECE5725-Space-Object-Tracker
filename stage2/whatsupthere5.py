'''
ECE 5725 Final Project
Authors: Pavel Berezovsky (pvb23), Haritha Muralidharan (hm535)
Stage 2: Multiprocessing Search of Satellites
Subpart: Global and Local Searches
'''

import subprocess
import time
from pyorbital.orbital import Orbital, OrbitalError, tlefile
from datetime import datetime
from multiprocessing import Process
from random import randint
import os
import errno


class GlobalSearch:
	'''
	Class for the Global Search. This class will search all the satellites, and
	identify those in the [-20,20] neighborhood of the desired center.
	To create an instance of Global Search, initialize with the search threshold
	in GPS degrees, the longitude and latitude of the center, and the path to
	the TLE files and static information files.

	We made these arguments for initialization so that future users can easily
	use the class for different systems without having to change the internal
	functionality of the class.
	'''
	def __init__(self, thresh, clon, clat, path):
		self.gps_threshold = thresh		# search window for the global search
		self.clon = clon							# center longitude based on user input
		self.clat = clat							# center latitude based on user input
		self.path = path							# path to TLE and other relevant files
		self.counter = 0							# counter for debugging
		self.running = True						# variable to turn the search on/off

		self.searchFiles = []					# list of files with offline static information
		self.tleFiles = []						# list of TLE files
		self.writeFiles = []					# list of output files

		# append all the files containing the static information
		self.searchFiles.append(self.path + '/good_engineering_sat.txt')
		self.searchFiles.append(self.path + '/good_globalstar_sat.txt')
		self.searchFiles.append(self.path + '/good_iridium_sat.txt')
		self.searchFiles.append(self.path + '/good_navy_sat.txt')
		self.searchFiles.append(self.path + '/good_orbcomm_sat.txt')
		self.searchFiles.append(self.path + '/good_active_sat.txt')

		# append the tle files
		self.tleFiles.append(self.path + '/satellites1a.txt') #engineering
		self.tleFiles.append(self.path + '/satellites2a.txt') #globalstar
		self.tleFiles.append(self.path + '/satellites3a.txt') #iridium
		self.tleFiles.append(self.path + '/satellites4a.txt') #navy
		self.tleFiles.append(self.path + '/satellites5a.txt') #orbcomm
		self.tleFiles.append(self.path + '/satellites0a.txt') #active

		# append the names of the output files
		self.writeFiles.append(self.path + '/local_engineering_sat.txt')
		self.writeFiles.append(self.path + '/local_globalstar_sat.txt')
		self.writeFiles.append(self.path + '/local_iridium_sat.txt')
		self.writeFiles.append(self.path + '/local_navy_sat.txt')
		self.writeFiles.append(self.path + '/local_orbcomm_sat.txt')
		self.writeFiles.append(self.path + '/local_active_sat.txt')

	# helper function to start the search
	def startSearch(self):
		self.running = True

	# helper function to stop the search
	def terminateSearch(self):
		self.running = False

	# helper function for new user inputs
	def changeCoordinates(self, newLon, newLat):
		self.clon = newLon
		self.clat = newLat

	# main search function
	def run(self): # run forever until terminated
		while(self.running):

			self.counter += 1

			# download the latest TLE files
			cmd = "wget -O " + self.path + "/satellites0a.txt 'https://www.celestrak.com/NORAD/elements/active.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites1a.txt 'https://www.celestrak.com/NORAD/elements/engineering.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites2a.txt 'https://www.celestrak.com/NORAD/elements/globalstar.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites3a.txt 'https://www.celestrak.com/NORAD/elements/iridium.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites4a.txt 'https://www.celestrak.com/NORAD/elements/nnss.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites5a.txt 'https://www.celestrak.com/NORAD/elements/orbcomm.txt'"
			subprocess.check_output(cmd, shell=True)

			#print('\n')

			# for each file in the search list
			for fileNum in range(0, len(self.searchFiles)):

				searchfile = self.searchFiles[fileNum]
				tlefile = self.tleFiles[fileNum]
				writefile = self.writeFiles[fileNum]

				file_object = open(searchfile, 'r')
				ifile = iter(file_object)

				# load all the static information as dictionaries for easy referencing
				# a new dictionary is created for each set of static information file
				name_to_func = {}
				name_to_unid = {}
				name_to_year = {}
				name_to_info = {}

				for item in ifile:
					n = item.find(':')
					s1 = item.find(',')
					s2 = item.find(',', s1+1)
					s3 = item.find(',', s2+1)

					unid = item[:n]
					name = item[n+1:s1]
					func = item[s1+1:s2]
					year = item[s2+1:s3]
					info = item[s3+1:].rstrip()

					name_to_func[name] = func
					name_to_unid[name] = unid
					name_to_year[name] = year
					name_to_info[name] = info

				file_object.close()

				# for every satellite in the static information file,
				# search the corresponding tle file, and get their longitude, latitude, altitude
				local_list = [] # list to append satellites in the search window
				for sat in name_to_unid:
					now = datetime.utcnow()
					try:
						# calls to the PyOrbital files to get the dynamic information
						orb = Orbital(sat, tlefile)
						(lon, lat, alt) = orb.get_lonlatalt(now)

					# error handling
					except OrbitalError:
						continue
					except NotImplementedError:
						continue
					except KeyError:
						continue

					# check if the satellite is in the search window
					if( abs(lon - clon) <= self.gps_threshold and abs(lat - clat) <= self.gps_threshold):
						# if it is, append the satellite and static information to the list
						# name, unique_id, function, year launched, launch number and piece, longitude, latitude, altitude
						tmp = [ sat, name_to_unid[sat], name_to_func[sat], name_to_year[sat], name_to_info[sat], lon, lat, alt]
						local_list.append(tmp)

				# write the list to the respective output files
				f = open(writefile, 'w')
				for item in local_list:
					entry = item[1] + ':' + item[0] + ',' + item[2] + ',' + item[3] + ',' + item[4]
					f.write(entry+'\n')
					#print(item)
				f.close()



class LocalSearch:
	'''
	Class for the Local Search. This class will search all the satellites, and
	identify those in the [-5,5] neighborhood of the desired center.
	To create an instance of Local Search, initialize with the search threshold
	in GPS degrees, the longitude and latitude of the center, and the path to
	the TLE files and static information files.

	We made these arguments for initialization so that future users can easily
	use the class for different systems without having to change the internal
	functionality of the class.
	'''
	def __init__(self, thresh, clon, clat, path):
		self.gps_threshold = thresh		# search window for the global search
		self.clon = clon							# center longitude based on user input
		self.clat = clat							# center latitude based on user input
		self.path = path							# path to TLE and other relevant files
		self.counter = 0							# counter for debugging
		self.running = True						# variable to turn the search on/off

		self.searchFiles = []					# list of files with offline static information
		self.tleFiles = []						# list of TLE files

		self.currentList = []					# list of satellites in the field of view
		self.previousList = {}				# dictionary for storing the RGB values for each sat


		# append all the files containing the static information
		self.searchFiles.append(self.path + '/local_engineering_sat.txt')
		self.searchFiles.append(self.path + '/local_globalstar_sat.txt')
		self.searchFiles.append(self.path + '/local_iridium_sat.txt')
		self.searchFiles.append(self.path + '/local_navy_sat.txt')
		self.searchFiles.append(self.path + '/local_orbcomm_sat.txt')
		self.searchFiles.append(self.path + '/local_active_sat.txt')

		# append the tle files
		self.tleFiles.append(self.path + '/satellites1b.txt') #engineering
		self.tleFiles.append(self.path + '/satellites2b.txt') #globalstar
		self.tleFiles.append(self.path + '/satellites3b.txt') #iridium
		self.tleFiles.append(self.path + '/satellites4b.txt') #navy
		self.tleFiles.append(self.path + '/satellites5b.txt') #orbcomm
		self.tleFiles.append(self.path + '/satellites0b.txt') #active

		# write files
		self.writeFile = self.path + '/local_satellites.txt' # for PiTFT
		self.writeFile2 = self.path + '/local_satellites2.txt' # for LED Matrix

	# helper function to start the search
	def startSearch(self):
		self.running = True

	# helper function to stop the search
	def terminateSearch(self):
		self.running = False
		# clear the rgb dictionary

	# helper function for new user inputs
	def changeCoordinates(self, newLon, newLat):
		print('The new coordinates are:', newLon, newLat)
		self.clon = newLon
		self.clat = newLat

	# main search function
	def run(self): # run forever until terminated
		while(self.running):
			self.counter += 1

			# download the latest TLE files
			cmd = "wget -O " + self.path + "/satellites0b.txt 'https://www.celestrak.com/NORAD/elements/active.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites1b.txt 'https://www.celestrak.com/NORAD/elements/engineering.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites2b.txt 'https://www.celestrak.com/NORAD/elements/globalstar.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites3b.txt 'https://www.celestrak.com/NORAD/elements/iridium.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites4b.txt 'https://www.celestrak.com/NORAD/elements/nnss.txt'"
			subprocess.check_output(cmd, shell=True)
			cmd = "wget -O " + self.path + "/satellites5b.txt 'https://www.celestrak.com/NORAD/elements/orbcomm.txt'"
			subprocess.check_output(cmd, shell=True)

			self.currentList = [] # list of satellites in the field of view

			# for each file in the search list
			for fileNum in range(0, len(self.searchFiles)):

				searchfile = self.searchFiles[fileNum]
				tlefile = self.tleFiles[fileNum]

				file_object = open(searchfile, 'r')
				ifile = iter(file_object)

				# load all the static information as dictionaries for easy referencing
				# a new dictionary is created for each set of static information file
				name_to_func = {}
				name_to_unid = {}
				name_to_year = {}
				name_to_info = {}

				for item in ifile:
					n = item.find(':')
					s1 = item.find(',')
					s2 = item.find(',', s1+1)
					s3 = item.find(',', s2+1)

					unid = item[:n]
					name = item[n+1:s1]
					func = item[s1+1:s2]
					year = item[s2+1:s3]
					info = item[s3+1:].rstrip()

					name_to_func[name] = func
					name_to_unid[name] = unid
					name_to_year[name] = year
					name_to_info[name] = info

				file_object.close()

				# for every satellite in the static information file,
				# search the corresponding tle file, and get their longitude, latitude, altitude
				for sat in name_to_unid:
					now = datetime.utcnow()
					try:
						# calls to the PyOrbital files to get the dynamic information
						orb = Orbital(sat, tlefile)
						(lon, lat, alt) = orb.get_lonlatalt(now)

					# error handling
					except OrbitalError:
						continue
					except NotImplementedError:
						continue
					except KeyError:
						continue

					# if it is, append the satellite and static information to the list
					if( abs(lon - clon) <= self.gps_threshold and abs(lat - clat) <= self.gps_threshold):
						# name, unique_id, function, year launched, launch number and piece, longitude, latitude, altitude
						# do some post-processing for displaying the name in a cleaner form
						# in the PiTFT
						np1 = sat.find('(')
						if np1 < 0: np1 = len(sat)
						np2 = sat.find('[')
						if np2 < 0: np2 = len(sat)
						np = min(np1, np2)
						name = sat[:np].rstrip()

						# check if the satellite is new or was already found
						if name in self.previousList:
							# if satellite was found before use the same colour
							satColor = self.previousList[name]
						else: # else generate a new rgb colour
							# the lower limit for the rgb is 30 because any number below that
							# is too dim on the LED matrix
							satColor = [randint(30,255),randint(30,255),randint(30,255)]
							self.previousList[name] = satColor

						# name, unique_id, function, year launched, launch number and piece, longitude, latitude, altitude
						tmp = [ name, name_to_unid[sat], name_to_func[sat], name_to_year[sat], name_to_info[sat], lon, lat, alt, satColor]
						self.currentList.append(tmp) # append to list

			# write all the found sats to the output files
			f = open(self.writeFile, 'w')
			for item in self.currentList:
				f.write(str(item)+'\n')
				#print(item)
			f.close()

			f = open(self.writeFile2, 'w')
			for item in self.currentList:
				f.write(str(item)+'\n')
			f.close()

			if (self.counter > 1000):
				self.counter = 0


# local path to be sent to the satellite search objects
path = "/home/pi/project/stage2"

# default lat and lon is washington dc
clon = 77.0369
clat = 38.9072
ip = 'test'

# initialize global search
globalSearch = GlobalSearch(20.0, clon, clat, path)
# initialize local search
localSearch = LocalSearch(5.0, clon, clat, path)

# read any incoming message from the fifo
# this gets user input for the center coordinates from the program
# handling on the PiTFT
fifoPath = "/home/pi/project/stage1_3/stage2_fifo"
bufferSize = 100
pipe = os.open(fifoPath, os.O_RDONLY)
ip = os.read(pipe, bufferSize)
#print('The recieved message is: ' + ip)

# start separate processes for each search
p1 = Process(target = globalSearch.run, args=())
p2 = Process(target = localSearch.run, args=())

p1.start()
p2.start()


while (True): # run forever

	# if user terminated the program
	if( ip and ip[0] == 'Q'):
		print('SATELLITE SEARCH TERMINATED')
		p1.terminate()
		p2.terminate()
		globalSearch.terminateSearch()
		localSearch.terminateSearch()
		break

	# if user changes new coordinates
	elif( ip ):
		# parse the coordinates
		print('The recieved message is: ' + ip)
		cs = ip.find(',')
		lon_s = ip[:cs]
		lat_s = ip[cs+1:]
		clon = float(lon_s)
		clat = float(lat_s)

		# stop the searches
		p1.terminate()
		p2.terminate()

		# change the center coordinates of each search
		globalSearch.changeCoordinates(clon, clat)
		localSearch.changeCoordinates(clon, clat)

		# restart the searches as separate process
		p1 = Process(target = globalSearch.run, args=())
		p2 = Process(target = localSearch.run, args=())
		p1.start()
		p2.start()

	ip = os.read(pipe, bufferSize) # monitor for any new user input

os.close(pipe)
