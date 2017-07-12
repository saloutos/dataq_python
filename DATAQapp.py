### DATAQapp.py ###
### Andrew SaLoutos, 7/7/2017

### This is a python script to control data acquisition through a GUI for a DI-149 module from Dataq Instruments

### With the "Submit new paramaeters" buttons/window, the user is expected to enable channels, set a desired sample rate and time, and pick an output location for the data (in .csv file format).
### The user should connect to the DI149, set any desired parameters, start scanning, and then quit the GUI.
### The status line at the bottom of the main GUI window tells the user whether the DI-149 is connected or disconnected. The command line windwo reads out whether data is being collected or being saved to the output file.
### The user can also observe the time that the last data collection run was completed, in the last line of the main GUI window.

### Import packages
import clr
import time
import csv
import numpy as np
import string
from tkinter import Toplevel, Tk, Label, Button, Checkbutton, Entry, StringVar, IntVar, BooleanVar, END, W, E, LEFT, RIGHT

### Load .dll files to interact with DI-149
clr.AddReference("System")
from System import Array

# Load Dataq.Common.dll
clr.AddReference('') # these filepaths could be subject to change, they must not be the original file location
from Dataq import *

# Load Dataq.Simple.dll
clr.AddReference('')
from Dataq.Simple import *

### Global variables for DI device
myDI = ''
DIHardware = ''
sampleTime = 0
data = []
t0 = 0
t1 = 0
folderpath = ''
filename = ''
params_window = ''
en1 = 0
en2 = 0
en3 = 0
en4 = 0
en5 = 0
en6 = 0
en7 = 0
en8 = 0

### Define GUI class, functions
class DATAQapp:

	def __init__(self, master): # initialization function
		self.master = master
		master.title("DI-149 Analog Data Aquisition")

		# Buttons to connect, start sampling, and disconnect
		self.connect_button = Button(master, text="Connect to DI-149!", command=self.connect, bg="green3")
		self.change_params_button = Button(master, text="Change sampling parameters!", command=self.open_params_window)
		self.start_button = Button(master, text="Start Scanning!", command=self.start, bg="green3")
		self.quit_button = Button(master, text="Quit!", command=self.shutdown, bg="red")

		# Status of program (not connected, connected, sampling data, saving data, etc)
		self.status_label = Label(master, text="Status: not connected")

		# Start time of last data collection
		self.last_run_label = Label(master, text="Last collection run at: no collection run yet")

		# LAYOUT
		self.connect_button.pack()
		self.change_params_button.pack()
		self.start_button.pack()
		self.quit_button.pack()

		self.status_label.pack()
		self.last_run_label.pack()




	# def validate(self, new_text): # function to validate user entries for parameters
	# 	if not new_text: # the field is being cleared
	# 		self.entered_number = 0
	# 		return True

	# 	try:
	# 		self.entered_number = int(new_text)
	# 		return True
	# 	except ValueError:
	# 		return False

	def open_params_window(self):
		global myDI, DIHardware, button_array, params_window, en1, en2, en3, en4, en5, en6, en7, en8

		print("New parameters!")
		params_window = Toplevel()
		params_window.title("Sampling Parameters")

		en1 = BooleanVar()
		en2 = BooleanVar()
		en3 = BooleanVar()
		en4 = BooleanVar()
		en5 = BooleanVar()
		en6 = BooleanVar()
		en7 = BooleanVar()
		en8 = BooleanVar()

		try:
			# Enable channels
			self.set_channels_label = Label(params_window, text="Enable Channels:")
			self.set_channels_label.pack()

			self.CH1 = Checkbutton(params_window, text=1, variable=en1)
			self.CH1.pack()
			if (DIHardware.ChannelArray[0].Enabled): self.CH1.select()

			self.CH2 = Checkbutton(params_window, text=2, variable=en2)
			self.CH2.pack()
			if (DIHardware.ChannelArray[1].Enabled): self.CH2.select()

			self.CH3 = Checkbutton(params_window, text=3, variable=en3)
			self.CH3.pack()
			if (DIHardware.ChannelArray[2].Enabled): self.CH3.select()

			self.CH4 = Checkbutton(params_window, text=4, variable=en4)
			self.CH4.pack()
			if (DIHardware.ChannelArray[3].Enabled): self.CH4.select()

			self.CH5 = Checkbutton(params_window, text=5, variable=en5)
			self.CH5.pack()
			if (DIHardware.ChannelArray[4].Enabled): self.CH5.select()

			self.CH6 = Checkbutton(params_window, text=6, variable=en6)
			self.CH6.pack()
			if (DIHardware.ChannelArray[5].Enabled): self.CH6.select()

			self.CH7 = Checkbutton(params_window, text=7, variable=en7)
			self.CH7.pack()
			if (DIHardware.ChannelArray[6].Enabled): self.CH7.select()

			self.CH8 = Checkbutton(params_window, text=8, variable=en8)
			self.CH8.pack()
			if (DIHardware.ChannelArray[7].Enabled): self.CH8.select()

			# Set sample rate
			self.set_sample_rate_label = Label(params_window, text="Sample rate per channel (Hz):")
			#vcmd = master.register(self.validate) # we have to wrap the command
			self.set_sample_rate_entry = Entry(params_window) #, validate="key", validatecommand=(vcmd, '%P'))
			self.set_sample_rate_label.pack()
			self.set_sample_rate_entry.pack()
			self.set_sample_rate_entry.insert(0, str(DIHardware.SampleRatePerChannel))

			# Set sample time
			self.set_sample_time_label = Label(params_window, text="Total sample time (s):")
			#vcmd = master.register(self.validate) # we have to wrap the command
			self.set_sample_time_entry = Entry(params_window)#, validate="key", validatecommand=(vcmd, '%P'))
			self.set_sample_time_label.pack()
			self.set_sample_time_entry.pack()
			self.set_sample_time_entry.insert(0, str(sampleTime))

			# # Set miminum number of samples
			# self.set_min_samples_label = Label(params_window, text="Minimum number of samples:")
			# self.set_min_samples_entry = Entry(params_window)
			# self.set_min_samples_label.pack()
			# self.set_min_samples_entry.pack()
			# self.set_min_samples_entry.insert(0, str(DIHardware.NewDataMinimum))

			# Set output folder
			self.set_output_folder_label = Label(params_window, text="Folder path for output:")
			#vcmd = master.register(self.validate) # we have to wrap the command
			self.set_output_folder_entry = Entry(params_window)#, validate="key", validatecommand=(vcmd, '%P'))
			self.set_output_folder_label.pack()
			self.set_output_folder_entry.pack()
			self.set_output_folder_entry.insert(0,folderpath)

			# Set output filename
			self.set_output_file_label = Label(params_window, text="Name of output file:")
			#vcmd = master.register(self.validate) # we have to wrap the command
			self.set_output_file_entry = Entry(params_window)#, validate="key", validatecommand=(vcmd, '%P'))
			self.set_output_file_label.pack()
			self.set_output_file_entry.pack()
			self.set_output_file_entry.insert(0, filename)

			# Button to set sampling parameters
			self.sample_params_button = Button(params_window, text="Submit sampling parameters!", command=self.submit_params, bg="green3")
			self.sample_params_button.pack()

		except AttributeError:
			print("Not connected...connect to the DI-149 first!")
			params_window.destroy()

	def submit_params(self):
		global myDI, DIHardware, sampleTime, filename, folderpath, button_array, params_window, en1, en2, en3, en4, en5, en6, en7, en8

		DIHardware.ChannelArray[0].Enabled = en1.get()
		print(DIHardware.ChannelArray[0].Enabled)
		DIHardware.ChannelArray[1].Enabled = en2.get()
		print(DIHardware.ChannelArray[1].Enabled)
		DIHardware.ChannelArray[2].Enabled = en3.get()
		print(DIHardware.ChannelArray[2].Enabled)
		DIHardware.ChannelArray[3].Enabled = en4.get()
		print(DIHardware.ChannelArray[3].Enabled)
		DIHardware.ChannelArray[4].Enabled = en5.get()
		print(DIHardware.ChannelArray[4].Enabled)
		DIHardware.ChannelArray[5].Enabled = en6.get()
		print(DIHardware.ChannelArray[5].Enabled)
		DIHardware.ChannelArray[6].Enabled = en7.get()
		print(DIHardware.ChannelArray[6].Enabled)
		DIHardware.ChannelArray[7].Enabled = en8.get()
		print(DIHardware.ChannelArray[7].Enabled)

		DIHardware.SampleRatePerChannel = float(self.set_sample_rate_entry.get())
		print('Sample rate is {} Hz'.format(DIHardware.SampleRatePerChannel))

		# DIHardware.NewDataMinimum = int(self.set_min_samples_entry.get())
		# print('New data minimum is {}'.format(DIHardware.NewDataMinimum))

		sampleTime = int(self.set_sample_time_entry.get())
		print('Sample time is {} s'.format(sampleTime))

		folderpath = self.set_output_folder_entry.get()
		filename = self.set_output_file_entry.get()
		print(folderpath)
		print(filename)

		print("Submitted!")

		params_window.destroy()

	def connect(self): # function to connect to DI-149 and set parameters
		print("Connecting...")
		global myDI, DIHardware, sampleTime, filename, folderpath
		try:
			myDI = Discovery.DiscoverAllDevices() # find DI-149 device
			DIHardware = myDI[0]
			while(DIHardware.get_IsConnected() == False): # wait to connect to device
				DIHardware.Connect()
			print("Connected!")

			### Set default parameters
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
			DIHardware.ChannelArray[9].Enabled = False
			# Set up the count input bit (DI3)
			DIHardware.ChannelArray[10].Enabled = False
			# Set up the digital outputs (DO0, DO1, DO2, DO3)
			DIHardware.ChannelArray[11].Write(0)

			# Set the Sample Rate in Hz
			DIHardware.SampleRatePerChannel = 80
			print('Sample rate is {} Hz'.format(DIHardware.SampleRatePerChannel))

			# Set the number of scans to acquire before the NewData event fires.
			DIHardware.NewDataMinimum = 10
			print('New data minimum is {}'.format(DIHardware.NewDataMinimum))

			# Set sample time in seconds (num samples is sample rate * sample time)
			sampleTime = 10
			print('Sample time is {} s'.format(sampleTime))

			# Save output data to .csv file
			folderpath = 'C:/Users/Andrew/Desktop/' # default folder path
			filename = 'new_data.csv' # default filename
			print(folderpath)
			print(filename)

			### Open params window to set params for the first time? Not needed with defaults?

			self.status_label['text'] = "Status: connected" # update status in app window


		except TypeError:
			print("Already connected!")

		except IndexError:
			print("Plug in the DI-149!")

	def shutdown(self):
		print("Disconnecting...")
		try:
			while(DIHardware.get_IsConnected()): DIHardware.Disconnect()
			print("Disconnected!\nQuitting...")
			root.destroy()
		except AttributeError:
			root.destroy()

	def start(self):
		global DIHardware, sampleTime, data, t0, t1, folderpath, filename

		NumChannels = DIHardware.NumberOfChannelsEnabled # find total number of enabled channels

		DIHardware.Start() # start collection
		print("Collecting data...")
		t0 = time.clock() # start time in seconds
		t1 = t0

		while t1 < (t0+sampleTime): # sampling loop
			if ((DIHardware.NewData != None) & (DIHardware.NumberOfScansAvailable > DIHardware.NewDataMinimum)): # check if there is enough data to sample
				Scans = DIHardware.NumberOfScansAvailable
				new_data_points = Array[float](([0]*NumChannels*Scans)) # set up .NET array for incoming data
				DIHardware.GetInterleavedScaledData(new_data_points, 0, Scans) # fill array with new data
				t1 = time.clock() # record timestamp of new data
				new_data_points = np.fromiter(new_data_points, float) # convert back to python array
				if (NumChannels > 1): # reshape for storage based on NumChannels
					new_data_points = np.reshape(new_data_points, (Scans,NumChannels))
				for point in range(Scans): # organize data collected at the same time in order to correctly append to master list
					List = [0]
					if (NumChannels > 1):
						for chan in range(NumChannels):
							List.append(new_data_points[point,chan])
					else:
						List.append(new_data_points[point])
					if (point == (Scans-1)):
						List[0] = t1-t0
						data.append(tuple(List))
					else:
						List[0] = None
						data.append(tuple(List))

		DIHardware.Stop() # stop the sampling
		print('Data points gathered: {}'.format(len(data))) # check that this matches the expected amount

		print('Saving data...') # Save output data to .csv file

		full_path = folderpath+filename # full path for output files

		header = ['Time']
		chan_num = 0
		for chan in DIHardware.ChannelArray:
			#print(chan)
			chan_num += 1
			if chan.Enabled:
				header.append('Channel {}'.format(chan_num))
		with open(full_path, 'w', newline='') as out:
			csv_out = csv.writer(out)
			csv_out.writerow(header)
			for row in data:
				csv_out.writerow(row)

		print('Finished collection run!')

		data = []

		self.status_label['text'] = "Status: data collected" # update status in app window
		self.last_run_label['text'] = "Last collection run at: "+time.strftime("%X") # update last run time in app window

	def greet(self):
		print("Greetings!")

### Start GUI interface / app
root = Tk()
my_gui = DATAQapp(root)
root.protocol("WM_DELETE_WINDOW", my_gui.shutdown)
root.mainloop()
