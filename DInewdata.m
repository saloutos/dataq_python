function DInewdata(DIHardware,DICallback)

% global myData;

%Get the number of available scans, channels, and samples (scans * enabled
%channels)
DI_AvailableScans = DIHardware.NumberOfScansAvailable
DI_EnabledChannels = DIHardware.NumberOfChannelsEnabled
DI_AvailableSamples = DI_AvailableScans * DI_EnabledChannels

%Create a .NET arrary to hold the data. If using GetInterleavedBinaryData
%define the array as System.Int16
DI_NArray = NET.createArray('System.Double',DI_AvailableSamples);
%DI_NArray = NET.createArray('System.Int16',DI_AvailableSamples);

%Fill the scaled data into the array.  
DIHardware.GetInterleavedScaledData(DI_NArray, 0, DI_AvailableScans);
%DIHardware.GetInterleavedBinaryData(DI_NArray, 0, DI_AvailableScans);

%Convert .NET array data to a double array with a row for each scan
% and a column for each enabled channel.
DI_NewData = reshape(DI_NArray.double,DI_EnabledChannels,[])';

%Display the data in the Command Window
disp(DI_NewData)
% myData = [myData; DI_NewData];

end