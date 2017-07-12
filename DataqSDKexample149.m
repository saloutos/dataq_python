%Example program for the DataqSDK.NET control with a DI-149 in MATLAB. 
%Prerequisites: WinDaq software installed, DI-149 hardware installed,
%DInewdata.m file.
%Please submit any questions about this program online at: http://www.dataq.com/support/live-agent/

%%% variable for storing collected data
% global myData;


%Make the .NET DATAQ SDK assembly visible to MATLAB
%The file path for the Dataq.Simple.dll and Dataq.Common.dll will vary
%depending on your OS and installation version.  
%The dll's will only need to be added the first time you run the program
asm1 = NET.addAssembly('C:\WINDOWS\Microsoft.NET\assembly\GAC_MSIL\Dataq.Simple\v4.0_1.0.0.2__9767f47f9c295223\Dataq.Simple.dll');
asm2 = NET.addAssembly('C:\WINDOWS\Microsoft.NET\assembly\GAC_MSIL\Dataq.Common\v4.0_1.0.0.1__9767f47f9c295223\Dataq.Common.dll');

%View the methods, properties and events of Dataq.Simple
methods Dataq.Simple.DataqDevice
properties Dataq.Simple.DataqDevice
events Dataq.Simple.DataqDevice

%Discover connected devices
myDI = Dataq.Simple.Discovery.DiscoverAllDevices;

%Use the first device in the discovery array
DIHardware = myDI(1);

%Connect to the DATAQ Hardware
%If the hardware was not detected you will get an error that the 'Index was
%outside the bounds of the array.'
try
  DIHardware.Connect();
catch ME
  disp(ME.message);
end

%Display the Serial Number, COMPort, and hardware model
disp(DIHardware.SerialNumber)
disp(DIHardware.ComPort)
disp(DIHardware.Model)
    
%DI-149 ChannelArray map:
%ChannelArray(1-8) analog inputs 1-8 
%ChannelArray(9) all digital inputs (all four bits)
%ChannelArray(10) frequency/rate input (DI2)
%ChannelArray(11) count input (DI3)
%ChannelArray(12) digital outputs (DO0, DO1, DO2, DO3)

%Enable Channels
DIHardware.ChannelArray(1).Enabled = false; 
DIHardware.ChannelArray(2).Enabled = true; 
DIHardware.ChannelArray(3).Enabled = false; 
DIHardware.ChannelArray(4).Enabled = false; 
DIHardware.ChannelArray(5).Enabled = false; 
DIHardware.ChannelArray(6).Enabled = false;
DIHardware.ChannelArray(7).Enabled = false; 
DIHardware.ChannelArray(8).Enabled = false; 

%Set up the digital inputs
DIHardware.ChannelArray(9).Enabled = false;

%Set up the rate input bit (DI2)
DIHardware.ChannelArray(10).InputRange = DIHardware.ChannelArray(10).ListOfInputRanges.Item(6);
DIHardware.ChannelArray(10).Enabled = false; 

%Set up the count input bit (DI3)
DIHardware.ChannelArray(11).Enabled = false; 

%Set up the digital outputs (DO0, DO1, DO2, DO3)
%Construct a value between 0-15 (4-bit) to write to the digital output port as a function of
%checked (enabled) bits. When a bit is checked the output is driven low (each is a low-true output)
%DO0 = 1, DO1 = 2, %DO2 = 4, DO3 = 8.  This example enables DO1 & DO2 (2+4)
DIHardware.ChannelArray(12).Write(6); 
%You can write the value to the ports asynchronously during data acq - type
%DIHardware.ChannelArray(12).Write(DigitalOutValue) in the Command Window
%Use the asynchrounous feature for real time alarms, etc.

%Set the Sample Rate
DIHardware.SampleRatePerChannel = 80;
%Display the actual Sample Rate. Note: the class will always select the sampling rate closest to the one selected constrained
%by the number of enabled channels. For a full treatment of how to configure DI-149 sampling rate refer to the instrument's prototocol document:
%http://www.dataq.com/resources/pdfs/misc/di-149-protocol.pdf
disp('Sample Rate Per Channel')
disp(DIHardware.SampleRatePerChannel)

%Set the number of scans to acquire before the NewData event fires.
DIHardware.NewDataMinimum = 10; 

%Create an event listener for the NewData event. 
%This event listener will run the code in the DInewdata.m file each time new data is available after the device is started. 
try
    lh = addlistener(DIHardware,'NewData',@DInewdata);
catch ME
    disp(ME.message);
end

%Start scanning
disp('Start scanning');
DIHardware.Start();

%Pause for 5 seconds to collect data.  The pause is used only for
%demonsration in this example file.  Comment out the 'DIHardware.Stop();'
%and 'DIHardware.Disconnect();' lines for continuous data collection and
%then execute these lines from the Command Window when you want to stop scanning.
pause(1);

%Stop scanning
DIHardware.Stop();

%It is important to disconnect from the device.  If you have connected
%successfully to the device, but do not disconnect you may need to unplug
%your hardware from the USB cable before you can connect again.  
DIHardware.Disconnect();
