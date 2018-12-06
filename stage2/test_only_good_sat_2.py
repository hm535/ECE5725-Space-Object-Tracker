'''
ECE 5725 Final Project
Authors: Pavel Berezovsky (pvb23), Haritha Muralidharan (hm535)
Stage 2: Multiprocessing Search of Satellites
Subpart: Offline computation of static information
'''

from pyorbital.orbital import Orbital, OrbitalError, tlefile
from datetime import datetime

'''
This file does the offline search and store for all the static information of the
active satellites. The output is five separate files containing the satellite names, their
unique ids, launch years, launch numbers, and function/ type.
'''
import subprocess

num_files = 38

# path to local directory - for toggling on different platforms
path = "/home/pi/project/stage2"

# All active satellites
cmd = "wget -O " + path + "/satellites0.txt 'https://www.celestrak.com/NORAD/elements/active.txt'"
subprocess.check_output(cmd, shell=True)

# Weather and Earth Resource Satellites
cmd = "wget -O " + path + "/satellites1.txt 'https://www.celestrak.com/NORAD/elements/weather.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites2.txt 'https://www.celestrak.com/NORAD/elements/resource.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites3.txt 'https://www.celestrak.com/NORAD/elements/cubesat.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites4.txt 'https://www.celestrak.com/NORAD/elements/dmc.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites5.txt 'https://www.celestrak.com/NORAD/elements/spire.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites6.txt 'https://www.celestrak.com/NORAD/elements/goes.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites7.txt 'https://www.celestrak.com/NORAD/elements/sarsat.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites8.txt 'https://www.celestrak.com/NORAD/elements/planet.txt'"
subprocess.check_output(cmd, shell=True)

# Communication Satellites
cmd = "wget -O " + path + "/satellites9.txt 'https://www.celestrak.com/NORAD/elements/geo.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites10.txt 'https://www.celestrak.com/NORAD/elements/intelsat.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites11.txt 'https://www.celestrak.com/NORAD/elements/iridium.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites12.txt 'https://www.celestrak.com/NORAD/elements/gorizont.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites13.txt 'https://www.celestrak.com/NORAD/elements/raduga.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites14.txt 'https://www.celestrak.com/NORAD/elements/molniya.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites15.txt 'https://www.celestrak.com/NORAD/elements/orbcomm.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites16.txt 'https://www.celestrak.com/NORAD/elements/ses.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites17.txt 'https://www.celestrak.com/NORAD/elements/amateur.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites18.txt 'https://www.celestrak.com/NORAD/elements/argos.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites19.txt 'https://www.celestrak.com/NORAD/elements/iridium-NEXT.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites20.txt 'https://www.celestrak.com/NORAD/elements/globalstar.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites21.txt 'https://www.celestrak.com/NORAD/elements/x-comm.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites22.txt 'https://www.celestrak.com/NORAD/elements/other-comm.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites23.txt 'https://www.celestrak.com/NORAD/elements/gps-ops.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites24.txt 'https://www.celestrak.com/NORAD/elements/glo-ops.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites25.txt 'https://www.celestrak.com/NORAD/elements/galileo.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites26.txt 'https://www.celestrak.com/NORAD/elements/beidou.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites27.txt 'https://www.celestrak.com/NORAD/elements/sbas.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites28.txt 'https://www.celestrak.com/NORAD/elements/nnss.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites29.txt 'https://www.celestrak.com/NORAD/elements/musson.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites30.txt 'https://www.celestrak.com/NORAD/elements/science.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites31.txt 'https://www.celestrak.com/NORAD/elements/geodetic.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites32.txt 'https://www.celestrak.com/NORAD/elements/engineering.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites33.txt 'https://www.celestrak.com/NORAD/elements/education.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites34.txt 'https://www.celestrak.com/NORAD/elements/military.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites35.txt 'https://www.celestrak.com/NORAD/elements/radar.txt'"
subprocess.check_output(cmd, shell=True)
cmd = "wget -O " + path + "/satellites36.txt 'https://www.celestrak.com/NORAD/elements/other.txt'"
subprocess.check_output(cmd, shell=True)
# cmd = "wget -O " + path + "/satellites37.txt 'https://www.celestrak.com/NORAD/elements/stations.txt'"
# subprocess.check_output(cmd, shell=True)



f = open("good_sat.txt","w+")
full_data_list = []
active_list = []
count = 0
bad_count = 0
satellite_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
bad_noaa_count = 0


satellite_list = []
unique_id_list = []

# only for active satellites
id_to_function = {}
id_to_name = {}
id_to_launch_year = {}
id_to_launch_info = {}

# to concatenate non active satellites
id_function_dict = {}

# Read the active satellites file and store all the ids and names
filename = path + '/satellites0.txt'
file_object = open(filename, 'r')
ifile = iter(file_object)
for sat in ifile:
	count += 1
	if( not sat[0].isdigit() ):
		sat = sat.strip('\n')
		sat = sat.rstrip()
		try:
			# check if any errors are raised
			now = datetime.utcnow()
			orb = Orbital(sat, filename)
			(lon,lat,alt) = orb.get_lonlatalt(now)
			tle = tlefile.read(sat, filename)

			# if no errors are raised, get the unique id and append
			item = next(ifile)
			s1 = item.find(' ')
			s2 = item.find(' ', s1+1)
			launch_id = item[s1+1:s2-1]

			if( int (tle.id_launch_year) >= 57 ):
				launch_year = '19' + str(tle.id_launch_year)
			else:
				launch_year = '20' + str(tle.id_launch_year)

			launch_info = str(tle.id_launch_number + tle.id_launch_piece)

			satellite_list.append(sat)
			unique_id_list.append(launch_id)



			# append dummy function
			if launch_id == '25544' or launch_id == '41765':
				id_function_dict[launch_id] = 'Space Station'
				id_to_function[launch_id] = 'Space Station'
			else:
				id_function_dict[launch_id] = 'null'
				id_to_function[launch_id] = 'null'

			id_to_name[launch_id] = sat
			id_to_launch_year[launch_id] = launch_year
			id_to_launch_info[launch_id] = launch_info

		except NotImplementedError:
				bad_count += 1
		except OrbitalError:
				bad_count += 1

satellite_count = []
known_satellites = 0
# Check the satellite functions
for i in range(1, num_files):
	filename = path + '/satellites' + str(i) + '.txt'
	file_object = open(filename, 'r')
	ifile = iter(file_object)
	# for every item in the current file
	# get its unique id
	# and change its function in the id_to_function dictionary
	count = 0
	for x in ifile:
		if( not x[0].isdigit() ):
			count += 1
			x = x.strip('\n')
			sat = x.rstrip()
			item = next(ifile)
			s1 = item.find(' ')
			s2 = item.find(' ', s1+1)
			launch_id = item[s1+1:s2-1]
			function = 'null'
			if i == 1:
				function = 'Weather'
			elif i == 2:
				function = 'Earth Resource'
			elif i == 3:
				function = 'Cube Satellites'
			elif i == 4:
				function = 'Disaster Monitoring'
			elif i == 5:
				function = 'Spire'
			elif i == 6:
				function = 'GOES' # none in active
			elif i == 7:
				function = 'Search and Rescue' # none in either list
			elif i == 8:
				function = 'Planet'
			elif i == 9:
				function = 'Geostationary' # none in active
			elif i == 10:
				function = 'Intelsat' # none in active
			elif i == 11:
				function = 'Iridium'
			elif i == 12:
				function = 'Gorizont' # none in active
			elif i == 13:
				function = 'Raduga' # none in active
			elif i == 14:
				function = 'Molniya' # none in active
			elif i == 15:
				function = 'Orbcom'
			elif i == 16:
				function = 'SES' # none in active
			elif i == 17:
				function = 'Amateur'
			elif i == 18:
				function = 'ARGOS'
			elif i == 19:
				function = 'Iridium-NEXT'
			elif i == 20:
				function = 'GlobalStar'
			elif i == 21:
				function = 'Experimental Communication'
			elif i == 22:
				function = 'Other Communication'
			elif i == 23:
				function = 'GPS Navigation' # none in active
			elif i == 24:
				function = 'GLONASS Navigation' # none in active
			elif i == 25:
				function = 'Galileo' # none in active
			elif i == 26:
				function = 'Beidou' # none in active
			elif i == 27:
				function = 'SBAS' # none in active
			elif i == 28:
				function = 'NNSS' # none in active
			elif i == 29:
				function = 'Russian LEO'
			elif i == 30:
				function = 'Science'
			elif i == 31:
				function = 'Geodetic'
			elif i == 32:
				function = 'Engineering'
			elif i == 33:
				function = 'Education'
			elif i == 34:
				function = 'Military'
			elif i == 35:
				function = 'Radar'
			elif i == 36:
				function = 'Other'
			# elif i == 37:
			# 	function = 'Space Stations'

			id_function_dict[launch_id] = function
			if launch_id in id_to_function:
				id_to_function[launch_id] = function

	satellite_count.append(count)
	known_satellites += count

print("Total # of satellites: " + str(len(id_function_dict))) #total num of satellites
print("Total # of active satellites: " + str(len(id_to_function))) #total num of active satellites
print("Total # of bad satellites: " + str(bad_count)) #num of bad satellites
print("Total # of Weather satellites: " + str(satellite_count[0]))
print("Total # of Earth Resource satellites: " + str(satellite_count[1]))
print("Total # of Cube Satellites satellites: " + str(satellite_count[2]))
print("Total # of Disaster Monitoring satellites: " + str(satellite_count[3]))
print("Total # of Spire satellites: " + str(satellite_count[4]))
print("Total # of GOES satellites: " + str(satellite_count[5]))
print("Total # of Search and Rescue satellites: " + str(satellite_count[6]))
print("Total # of Planet satellites: " + str(satellite_count[7]))
print("Total # of Geostationary satellites: " + str(satellite_count[8]))
print("Total # of Intelsat satellites: " + str(satellite_count[9]))
print("Total # of Iridium satellites: " + str(satellite_count[10]))
print("Total # of Iridium-NEXT satellites: " + str(satellite_count[18]))
print("Total # of Gorizont satellites: " + str(satellite_count[11]))
print("Total # of Raduga satellites: " + str(satellite_count[12]))
print("Total # of Molniya satellites: " + str(satellite_count[13]))
print("Total # of Orbcom satellites: " + str(satellite_count[14]))
print("Total # of SES satellites: " + str(satellite_count[15]))
print("Total # of Amateur satellites: " + str(satellite_count[16]))
print("Total # of ARGOS satellites: " + str(satellite_count[17]))
print("Total # of GlobalStar satellites: " + str(satellite_count[18]))
print("Total # of Experimental Communication satellites: " + str(satellite_count[19]))
print("Total # of Other Communication satellites: " + str(satellite_count[20]))
print("Total # of GPS satellites: " + str(satellite_count[21]))
print("Total # of GLONASS satellites: " + str(satellite_count[22]))
print("Total # of Galileo satellites: " + str(satellite_count[23]))
print("Total # of Beidou satellites: " + str(satellite_count[24]))
print("Total # of SBAS satellites: " + str(satellite_count[25]))
print("Total # of NNSS satellites: " + str(satellite_count[26]))
print("Total # of Russian LEO satellites: " + str(satellite_count[27]))
print("Total # of Science satellites: " + str(satellite_count[28]))
print("Total # of Geodetic satellites: " + str(satellite_count[29]))
print("Total # of Engineering satellites: " + str(satellite_count[30]))
print("Total # of Education satellites: " + str(satellite_count[31]))
print("Total # of Military satellites: " + str(satellite_count[32]))
print("Total # of Radar satellites: " + str(satellite_count[33]))
print("Total # of Other/ Misc satellites: " + str(satellite_count[34]))
# print("Total # of Space Stations: " + str(satellite_count[35]))


filename = "good_sat.txt"
f = open(filename, 'w')

for key in id_function_dict:
	f.write( str(key) + ':' + str(id_function_dict[key]) + '\n')

f.close()

filename = "good_active_sat.txt"
f = open(filename, 'w')

for key in id_to_function:
	entry = str(key) +  ':' + str( id_to_name[key] ) + ',' + str(id_function_dict[key]) + ',' + str(id_to_launch_year[key]) + ',' + str(id_to_launch_info[key]) + '\n'
	f.write(  entry )
f.close()
