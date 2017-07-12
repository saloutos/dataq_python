### tkinter test script

### from http://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html

# from tkinter import Tk, Label, Button, LEFT, RIGHT, W

# class MyFirstGUI:
#     def __init__(self, master):
#         self.master = master
#         master.title("A simple GUI")

#         self.label = Label(master, text="This is our first GUI!")
#         #self.label.pack()
#         self.label.grid(columnspan=2, sticky=W)

#         self.greet_button = Button(master, text="Greet", command=self.greet)
#         #self.greet_button.pack(side=LEFT)
#         self.greet_button.grid(row=1)

#         self.close_button = Button(master, text="Close", command=master.quit)
#         #self.close_button.pack(side=RIGHT)
#         self.close_button.grid(row=1, column=1)

#     def greet(self):
#         print("Greetings!")

# root = Tk()
# my_gui = MyFirstGUI(root)
# root.mainloop()

# from tkinter import Tk, Label, Button, StringVar

# class MyFirstGUI:
#     LABEL_TEXT = [
#         "This is our first GUI!",
#         "Actually, this is our second GUI.",
#         "We made it more interesting...",
#         "...by making this label interactive.",
#         "Go on, click on it again.",
#     ]
#     def __init__(self, master):
#         self.master = master
#         master.title("A simple GUI")

#         self.label_index = 0
#         self.label_text = StringVar()
#         self.label_text.set(self.LABEL_TEXT[self.label_index])
#         self.label = Label(master, textvariable=self.label_text)
#         self.label.bind("<Button-1>", self.cycle_label_text)
#         self.label.pack()

#         self.greet_button = Button(master, text="Greet", command=self.greet)
#         self.greet_button.pack()

#         self.close_button = Button(master, text="Close", command=master.quit)
#         self.close_button.pack()

#     def greet(self):
#         print("Greetings!")

#     def cycle_label_text(self, event):
#         self.label_index += 1
#         self.label_index %= len(self.LABEL_TEXT) # wrap around
#         self.label_text.set(self.LABEL_TEXT[self.label_index])

# root = Tk()
# my_gui = MyFirstGUI(root)
# root.mainloop()

# from tkinter import Tk, Label, Button, Checkbutton, Entry, IntVar, BooleanVar, END, W, E, LEFT, RIGHT

# array = [True, True, True, True, True, True, True, True]

# class DATAQapp:

#     def __init__(self, master):
#         self.master = master
#         master.title("DI-149 Analog Data Aquisition")

#         # Enable channels
#         self.set_channels_label = Label(master, text="Enable Channels:")
#         for element in range(8):
#         	array[element] = BooleanVar()
#         	C = Checkbutton(master, text=(element+1), variable=array[element])
#         	C.pack()

#         # Set sample rate
#         self.set_sample_rate_label = Label(master, text="Sample rate per channel:")
#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.set_sample_rate_entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

#         # Set sample time
#         self.set_sample_time_label = Label(master, text="Total sample time:")
#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.set_sample_time_entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

#         # Set output folder
#         self.set_output_folder_label = Label(master, text="Folder for output:")
#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.set_output_folder_entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

#         # Set output filename
#         self.set_output_file_label = Label(master, text="Name of output file:")
#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.set_output_file_entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

#         # Button to set sampling parameters
#         self.sample_params_button = Button(master, text="Submit", command=self.greet)

#         # Buttons to connect, start sampling, and disconnect
#         self.connect_button = Button(master, text="Connect", command=self.greet)
#         self.disconnect_button = Button(master, text="Disconnect", command=master.quit)
#         self.start_button = Button(master, text="Start Scanning!", command=self.greet)

#         # Status of program (not connected, connected, sampling data, saving data, etc)
#         self.status_label = Label(master, text="status goes here")

#         ### LAYOUT

#         self.set_channels_label.pack()
#         self.set_sample_rate_label.pack()
#         self.set_sample_rate_entry.pack()
#         self.set_sample_time_label.pack()
#         self.set_sample_time_entry.pack()
#         self.set_output_folder_label.pack()
#         self.set_output_folder_entry.pack()
#         self.set_output_file_label.pack()
#         self.set_output_file_label.pack()
#         self.sample_params_button.pack()

#         self.connect_button.pack()
#         self.disconnect_button.pack()
#         self.start_button.pack()
#         self.status_label.pack()

#         # self.label.grid(row=0, column=0, sticky=W)
#         # self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)

#         # self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

#         # self.add_button.grid(row=2, column=0)
#         # self.subtract_button.grid(row=2, column=1)
#         # self.reset_button.grid(row=2, column=2, sticky=W+E)

#     def validate(self, new_text):
#         if not new_text: # the field is being cleared
#             self.entered_number = 0
#             return True

#         try:
#             self.entered_number = int(new_text)
#             return True
#         except ValueError:
#             return False

#     def greet(self):
#         print("Greetings!")

# root = Tk()
# my_gui = DATAQapp(root)
# root.mainloop()


		# self.label.grid(row=0, column=0, sticky=W)
		# self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)

		# self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

		# self.add_button.grid(row=2, column=0)
		# self.subtract_button.grid(row=2, column=1)
		# self.reset_button.grid(row=2, column=2, sticky=W+E)

from tkinter import *
master = Tk()
var1 = IntVar()
Checkbutton(master, text="male", variable=var1).grid(row=0, sticky=W)
var2 = IntVar()
Checkbutton(master, text="female", variable=var2).grid(row=1, sticky=W)
mainloop()