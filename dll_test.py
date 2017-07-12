# File to test importing Dataq dlls with Python to .NET lib

import clr
import time
import random
import csv
import numpy as np
import string

clr.AddReference("System")
from System import Array

clr.AddReference('C:/Users/Andrew/Documents/Tanvas/Dataq/DataqDLLs/Dataq.Common.dll') # files cannot be in the original program location
from Dataq import * # can use asterisk to import all lower classes and functions without any loss

clr.AddReference('C:/Users/Andrew/Documents/Tanvas/Dataq/DataqDLLs/Dataq.Simple.dll')
from Dataq.Simple import *

clr.AddReference('C:/Users/Andrew/Documents/Tanvas/Dataq/DataqDLLs/DataqNet.dll')
from Dataq.Devices import DI149
# print(ChannelType) # experimenting with classes and functions
# print(TCTypeName.S)
# print(Discovery)
# print(Discovery.DiscoverAllDevices)


myDI = Discovery.DiscoverAllDevices()
# print(myDI[0])

DIHardware = myDI[0]
print(dir(DIHardware)) # show methods for the connected DI device

DIHardware.Connect()
print('Is DIHardware connected?')
print(DIHardware.get_IsConnected())
print('\n')
### throw error here if device is not connected

print('Serial number, COM port, Model')
print(DIHardware.SerialNumber)
print(DIHardware.ComPort)
print(DIHardware.Model)
print('\n')

# print(dir(DIHardware.ChannelArray[0]))

# Enable input channels
DIHardware.ChannelArray[0].Enabled = True
DIHardware.ChannelArray[1].Enabled = True 
DIHardware.ChannelArray[2].Enabled = False 
DIHardware.ChannelArray[3].Enabled = False
DIHardware.ChannelArray[4].Enabled = False 
DIHardware.ChannelArray[5].Enabled = False
DIHardware.ChannelArray[6].Enabled = False 
DIHardware.ChannelArray[7].Enabled = False

# Enable digital input
DIHardware.ChannelArray[8].Enabled = False

# Set up the rate input bit (DI2) 
#print(dir(DIHardware.ChannelArray[9].ListOfInputRanges))
# DIHardware.ChannelArray[9].InputRange = DIHardware.ChannelArray[9].ListOfInputRanges.Item(6) ### what does this do???
DIHardware.ChannelArray[9].Enabled = False

# Set up the count input bit (DI3)
DIHardware.ChannelArray[10].Enabled = False

# Set up the digital outputs (DO0, DO1, DO2, DO3)
# Construct a value between 0-15 (4-bit) to write to the digital output port as a function of
# checked (enabled) bits. When a bit is checked the output is driven low (each is a low-true output)
# DO0 = 1, DO1 = 2, %DO2 = 4, DO3 = 8.  This example enables DO1 & DO2 (2+4)
DIHardware.ChannelArray[11].Write(0) 
# You can write the value to the ports asynchronously during data acq - type
# DIHardware.ChannelArray(12).Write(DigitalOutValue) in the Command Window
# Use the asynchrounous feature for real time alarms, etc.

#for channel in DIHardware.ChannelArray: print(channel.Enabled)

# Set the Sample Rate
DIHardware.SampleRatePerChannel = 80
# Display the actual Sample Rate. Note: the class will always select the sampling rate closest to the one selected constrained
# by the number of enabled channels. For a full treatment of how to configure DI-149 sampling rate refer to the instrument's prototocol document:
# http://www.dataq.com/resources/pdfs/misc/di-149-protocol.pdf
print('Sample Rate Per Channel')
print(DIHardware.SampleRatePerChannel)
print('\n')

# Set the number of scans to acquire before the NewData event fires.
DIHardware.NewDataMinimum = 10
print('New Data Minimum')
print(DIHardware.NewDataMinimum)
print('\n')

# Set up parameters for sampling
NumChannels = DIHardware.NumberOfChannelsEnabled
print('Number of Channels Enabled')
print(NumChannels)
print('\n')

# Set sample time in seconds (num samples is sample rate * sample time)
sampleTime = 10
print('Sample time (in s)')
print(sampleTime)
print('\n')


# Sampling
print('Sampling...\n')
data = [] # list for collected data

DIHardware.Start()

t0 = time.clock() # start time in seconds
t1 = t0

# # Set up for NewData event
# def handler(source, args): ### what the fuck is going on here
# 	print('New data!')
# 	print(t0)
# 	Scans = DIHardware.NumberOfScansAvailable
# 	if Scans > 0:
# 		print('Scans:')
# 		print(Scans)
# 		new_data_points = Array[float](NumChannels*Scans)
# 		DIHardware.GetInterleavedScaledData(new_data_points, 0, Scans)
# 		#DIHardware.GetInterleavedBinaryData(new_data_points, 0, Scans)
# 		t1 = time.clock()
# 		data.append((t1-t0, new_data_points))

# d = DIHardware.NewDataEventHandler(handler)
# DIHardware.NewData += d

#### Sampling loop
#print(dir(DIHardware.NewData))
while t1 < sampleTime:
	if ((DIHardware.NewData != None) & (DIHardware.NumberOfScansAvailable > DIHardware.NewDataMinimum)):
		#print('New data!')
		Scans = DIHardware.NumberOfScansAvailable
		#print(NumChannels)
		#print(Scans)
		new_data_points = Array[float](([0]*NumChannels*Scans)) # set up .NET array
		DIHardware.GetInterleavedScaledData(new_data_points, 0, Scans)
		#DIHardware.GetInterleavedBinaryData(new_data_points, 0, Scans)
		t1 = time.clock()
		if (NumChannels > 1):
			new_data_points = np.fromiter(new_data_points, float) # convert back to python array
			new_data_points = np.reshape(new_data_points, (Scans,NumChannels)) # reshape for storage based on NumChannels
			print(new_data_points)
		for point in range(Scans):
			List = [0]
			for chan in range(NumChannels):
				List.append(new_data_points[point,chan])
			#print(point)
			if (point == (Scans-1)):
				List[0] = t1-t0
				data.append(tuple(List))
			else:
				List[0] = None
				data.append(tuple(List))
		#print(t1)

DIHardware.Stop()

print('Start and stop times')
print(t0)
print(t1)
print('\n')

print('Data points gathered:')
print(len(data))
print('\n')

# print('Data array')
# print(data)
# print('\n')

# Save output data to .csv file
print('Saving data...\n')
filename = 'new_data.csv' # name file here
filepath = 'C:/Users/Andrew/Desktop/'+filename # full path for output files

header = ['Time']
chan_num = 0
for chan in DIHardware.ChannelArray:
	#print(chan)
	chan_num += 1
	if chan.Enabled: 
		header.append('Channel {}'.format(chan_num))
print(header)

with open(filepath, 'w', newline='') as out:
	csv_out = csv.writer(out)
	csv_out.writerow(header)
	for row in data:
		csv_out.writerow(row)

# It is important to disconnect from the device.  If you have connected
# successfully to the device, but do not disconnect you may need to unplug
# your hardware from the USB cable before you can connect again.  
DIHardware.Disconnect()
print('Is DIHardware disconnected?')
print(DIHardware.get_IsConnected() == False)
print('\n')