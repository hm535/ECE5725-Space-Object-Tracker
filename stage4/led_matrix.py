'''
ECE 5725 Final Project
Authors: Pavel Berezovsky (pvb23), Haritha Muralidharan (hm535)
Stage 4: Serial Communication to Aruino/LED Matrix
Sub-Part: Including additional satellite files for search
'''
import os
import subprocess
import time
import serial

# Class to obtain satellite information
class LED_Data:
	def __init__(self,item):
        ''' The initilization of class takes 1 input parameter:
            item is a line from the local_satellites2.txt that contains
            information about one satellite
        '''
		self.longitude = str(item[5].strip()) # Saving satellite longitude
		self.latitude = str(item[6].strip()) # Saving satellite latitude
		temp = item[10].find(']')
        # Saving satellite RGB color
		self.color = [int(item[8][2:]),int(item[9].strip()),int(item[10][:temp])]
        # Initilizing x and y which are the mapped coordinates of the LED matrix
		self.x = 0 # x is row
		self.y =  # y is column

	def calc(self,long_map,lat_map):
        ''' THe function calc has 2 input parameters:
            long_map is a list of search intervals in the long direction
            lat_map is a list of search intervals in the lat direction

            The purpose of the function is to map the long and lat coordinates
            of a satellite to 16x16 LED matrix
        '''
		for i in range(1,len(long_map)):
			if(float(self.longitude) <=long_map[i]):
				self.x = i-1
				break;
		for i in range(1,len(lat_map)):
			if(float(self.latitude) <=lat_map[i]):
				self.y = 15-(i-1)
				break;
# # read any incoming message from the fifo
fifoPath = "/home/pi/project/stage1_3/stage4_fifo"
bufferSize = 100
pipe = os.open(fifoPath, os.O_RDONLY)
ip = os.read(pipe, bufferSize)
	#print('The recieved message is: ' + ip)
path = "/home/pi/project/stage2"
readfilename = path + '/local_satellites2.txt'

port = '/dev/ttyS0' # port for serial communication on RPi
rate = 9600 # Baud rate
s1 = serial.Serial(port,rate)

# Initilizing list
sat_list = []
center = []
bounds = []
long_map = []
lat_map = []
# Delimeter characters for serial transimission
start_full = chr(20)
start_local = chr(21)
end_local = chr(23)
end_full = chr(24)
end_display = chr(22)
while (True):
	if( ip and ip[0] == 'Q'): # If quit then end program and send quit to Arduino
		print('SATELLITE LED DISPLAY TERMINATED')
		s1.write(end_display)
		break
	elif( ip ): # If new coordinates recieved
		print('The recieved message is: ' + ip)
		cs = ip.find(',')
		lon_s = ip[:cs]
		lat_s = ip[cs+1:]

		center = [float(lon_s),float(lat_s)] # Center coordinates
		bounds = [center[0]-5.0,center[1]-5.0] # Lower bound for long and lat
		inc = 10.0/(16.0); # Incriment for search list
        # Making a list of seach intervals
		long_map = [bounds[0]]
		lat_map = [bounds[1]]
		for i in range(1,17):
			long_map.append(long_map[i-1]+inc)
			lat_map.append(lat_map[i-1]+inc)
    # Reading satellite information from the txt file
    sat_list = []
	file_object = open(readfilename, 'r')
	ifile = iter(file_object)
	for item in ifile:
		item = list(item.split(','))
		sat_list.append(LED_Data(item))
        
    # Calculating x,y position on LED matrix
	for i in range(0,len(sat_list)):
		sat_list[i].calc(long_map,lat_map)

    # Transmitting x,y,R,G,B to Arduino
	s1.write(start_full)
	for i in range(0,len(sat_list)):
		s1.write(start_local)
		s1.write(chr(sat_list[i].x))
		s1.write(chr(sat_list[i].y))
		s1.write(chr(sat_list[i].color[0]))
		s1.write(chr(sat_list[i].color[1]))
		s1.write(chr(sat_list[i].color[2]))
		s1.write(end_local)
	s1.write(end_full)
	time.sleep(1)

	ip = os.read(pipe, bufferSize)


os.close(pipe)
