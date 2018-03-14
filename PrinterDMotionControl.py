import serial
import Tkinter
import time
import datetime

from Tkinter import *
from time import sleep

#Connecting to the Arduino at a baudrate of 115200
try:
	ser = serial.Serial('COM7',115200,timeout = 2)
	print("Connection to motor/voltage Arduino Mega successful\n")
except Exception as e:
	print(e)
try:
	tempHumiditySerial = serial.Serial('COM5',9600,timeout = 2)
	print("Connection to sensor Arduino Uno successful\n")
	UnoConnect = True
except Exception as e:
	print(e)
	UnoConnect = False
	

xcoor = 0.0
ycoor = 0.0
zcoor = 0.0
#ucoor = 0.0 #Removed this line for printer D
#ztotcoor = zcoor + ucoor #Removed this line for printer D
dots = '0'
rasters = '0'
rasterCoor = '@';
timeType = True
xpitch = 0.0
ypitch = 0.0
dcRasterLength = 0.0
dcRasterPitch = 0.0
rasterRunning = False
fileName = ""
function = ""
functionRunning = False
fileInProcess = False
functionRunningRead = ""
fileConversionDone = False
mmToJogDist = 118.75
JogDistTomm = 0.00842105263157895

#Creating file for recording temperature and humidity
tempHumidityFile = open('Temperature Humidity Data.txt','w')
tempHumidityFile.write("Time	Humidity	Temperature\n")

# TODO:
# Measure ratio between steps and millimeters on printer
# attempt to receive feedback from arduino - so that we know when it completes a jog command
# Each marking is one milimeter

#Sending the desired jog distance to the Arduino. Have to write in how to convert from distance to # of steps
def get_xjogentry(event = None):
	print("XJOG DISTANCE: " + xjogentry.get())
	xconversion = float(xjogentry.get()) * mmToJogDist
	# ser.write('x' + str(xconversion))
	print('x' + xjogentry.get())
	set_xcoor()

def get_yjogentry(event=None):
	print(yjogentry.get())
	yconversion = float(yjogentry.get()) * mmToJogDist
	# ser.write('y' + str(yconversion))
	print('y' + str(yconversion))
	set_ycoor()

def get_zjogentry(event=None):
	print(zjogentry.get())
	zconversion = float(zjogentry.get()) * mmToJogDist
	# ser.write('z' + str(zconversion))
	print('z' + str(zconversion))
	set_zcoor()

def reset_origin(event=None):
	global xcoor
	global ycoor
	global zcoor
	print("RESET ORIGIN")
	xcoor = 0
	xcoorEntry.delete(0,END)
	xcoorEntry.insert(10, '{:+.3f}'.format(xcoor))
	ycoor = 0
	ycoorEntry.delete(0,END)
	ycoorEntry.insert(10, '{:+.3f}'.format(ycoor))
	zcoor = 0
	zcoorEntry.delete(0,END)
	zcoorEntry.insert(10, '{:+.3f}'.format(zcoor))

#Removed this section for printer D
# def get_ujogentry(event=None):
	# print(ujogentry.get())
	# ser.write('u' + ujogentry.get())
	# set_ucoor()
	
#Turning on and off the light
def light_switch(event = None):
	ser.write('w')
	
#Outputting the current coordinate system
def set_xcoor(event=None):
	global xcoor
	print(xcoor)
	xcoor = xcoor + float(xjogentry.get())
	xcoorEntry.delete(0,END)
	xcoorEntry.insert(10, '{:+.3f}'.format(xcoor))
	
def set_ycoor(event=None):
	global ycoor
	ycoor = ycoor + float(yjogentry.get())
	ycoorEntry.delete(0,END)
	ycoorEntry.insert(10, '{:+.3f}'.format(ycoor))
	
def set_zcoor(event=None):
	global zcoor
	#global ucoor #Removed this line for printer D
	global ztotcoor
	zcoor = zcoor + float(zjogentry.get())
	#ztotcoor = zcoor + ucoor #Removed this line for printer D
	zcoorEntry.delete(0,END)
	zcoorEntry.insert(10, '{:+.3f}'.format(zcoor))
	#ztotcoorEntry.delete(0,END) #Removed this line for printer D
	#ztotcoorEntry.insert(10, '{:+.3f}'.format(ztotcoor)) #Removed this line for printer D

#Removed this section for printer D	
# def set_ucoor(event=None):
	# global zcoor
	# global ucoor
	# global ztotcoor
	# ucoor = ucoor + float(ujogentry.get())
	# ztotcoor = zcoor + ucoor
	# ucoorEntry.delete(0,END)
	# ucoorEntry.insert(10, '{:+.3f}'.format(ucoor))
	# ztotcoorEntry.delete(0,END)
	# ztotcoorEntry.insert(10, '{:+.3f}'.format(ztotcoor))
	
	
#Resetting the coordinate system
#Resets x coordinate
def get_newxcoorEntry(event=None):
	global xcoor
	
	if newxcoorEntry.get():
		xcoor = float(newxcoorEntry.get())
		xcoorEntry.delete(0,END)
		xcoorEntry.insert(10, '{:+.3f}'.format(xcoor))

#Resets y coordinate
def get_newycoorEntry(event=None):
	global ycoor
	
	if newycoorEntry.get():
		ycoor = float(newycoorEntry.get())
		ycoorEntry.delete(0,END)
		ycoorEntry.insert(10, '{:+.3f}'.format(ycoor))
		
#Resets z and total vertical coordinate
def get_newzcoorEntry(event=None):
	global zcoor
	#global ucoor #Removed this line for printer D
	#global ztotcoor #Removed this line for printer D
	
	if newzcoorEntry.get():
		zcoor = float(newzcoorEntry.get())
		zcoorEntry.delete(0,END)
		zcoorEntry.insert(10, '{:+.3f}'.format(zcoor))
	#Removed this section for printer D
	#The next 3 lines update the total vertical coordinate value
	# ztotcoor = zcoor + ucoor
	# ztotcoorEntry.delete(0,END)
	# ztotcoorEntry.insert(10, '{:+.3f}'.format(ztotcoor))
	
#Removed this section for printer D
#Resets u and total vertical coordinate
# def get_newucoorEntry(event=None):
	# global zcoor
	# global ucoor
	# global ztotcoor
	
	# if newucoorEntry.get():
		# ucoor = float(newucoorEntry.get())
		# ucoorEntry.delete(0,END)
		# ucoorEntry.insert(10, '{:+.3f}'.format(ucoor))
	#The next 3 lines update the total vertical coordinate value
	# ztotcoor = zcoor + ucoor
	# ztotcoorEntry.delete(0,END)
	# ztotcoorEntry.insert(10, '{:+.3f}'.format(ztotcoor))
	
#Resets all of the coordinates simultaneously
def get_newCoordinatesEntry():
	global xcoor
	global ycoor
	global zcoor
	#global ucoor #Removed this line for printer D
	#global ztotcoor #Removed this line for printer D
	
	get_newxcoorEntry()
	get_newycoorEntry()
	get_newzcoorEntry()
	#get_newucoorEntry() #Removed this line for printer D

	
#Sending the high and low voltage levels to the Arduino
def get_highVoltageEntry(*event):
	print("High Voltage: " + highVoltageEntry.get())
	ser.write('vh' + highVoltageEntry.get())
	
def get_lowVoltageEntry(*event):
	print("Low Voltage: " + lowVoltageEntry.get())
	ser.write('vl' + lowVoltageEntry.get())
	
def turnOnHighVoltage(*event):
	print("Sending high voltage of " + highVoltageEntry.get() + "V")
	ser.write('vh' + highVoltageEntry.get()+'oh')
	
def turnOnLowVoltage(*event):
	print("Sending low voltage of " + lowVoltageEntry.get() + "V")
	ser.write('vl' + lowVoltageEntry.get()+'ol')

	
#Sending the pulse width on and off time to the Arduino
def get_onTimeEntry(*event):
	print("Pulse on time: " + onTimeEntry.get())
	ser.write('th' + onTimeEntry.get())

def get_offTimeEntry(*event):
	print("Pulse off time: " + offTimeEntry.get())
	ser.write('tl' + offTimeEntry.get())
	
#Sending the delay between steps to the Arduino
def get_stepDelayEntry(*event):
	print("Step Delay time: " + stepDelayEntry.get())
	ser.write('s' + stepDelayEntry.get())
	print("motor speed set")
	
	
#Sending the x and y pitch between drops to the Arduino
def get_xPitchEntry(*event):
	global xpitch
	print("X Pitch: " + xPitchEntry.get())
	xpitch = float(xPitchEntry.get())
	ser.write('px' + xPitchEntry.get())

def get_yPitchEntry(*event):
	global ypitch
	print("Y Pitch: " + yPitchEntry.get())
	ypitch = float(yPitchEntry.get())
	ser.write('py' + yPitchEntry.get())
	
#Sending the dc raster length to the Arduino
def get_dcRasterLengthEntry(*event):
	global dcRasterLength
	print("DC Raster Length: " + dcRasterLengthEntry.get())
	dcRasterLength = float(dcRasterLengthEntry.get())
	ser.write('cx' + dcRasterLengthEntry.get())

def get_dcRasterPitchEntry(*event):
	global dcRasterPitch
	print("DC Raster Pitch: " + dcRasterPitchEntry.get())
	dcRasterPitch = float(dcRasterPitchEntry.get())
	ser.write('cy' + dcRasterPitchEntry.get())

#Storing the desired number of dots and rasters
def get_dotsEntry(*event):
	global dots
	dots = dotsEntry.get()
	print("Dots: " + dots)
	if len(dots)==1:
		dots = '0' + dots

def get_rastersEntry(*event):
	global rasters
	print("Rasters: " + rastersEntry.get())
	rasters = rastersEntry.get()	
	
#Sending raster command to the Arduino
def sendRaster():
	global dots
	global rasters
	global rasterRunning
	rasterRunning = True
	get_highVoltageEntry()	#Sends current value in high voltage entry window to the Arduino
	get_lowVoltageEntry()	#Sends current value in low voltage entry window to the Arduino
	get_onTimeEntry()	#Sends current value in on time entry window to the Arduino
	get_offTimeEntry()	#Sends current value in off time entry window to the Arduino
	get_xPitchEntry()	#Sends current value in X Pitch entry window to the Arduino
	get_yPitchEntry()	#Sends current value in the Y Pitch entry window to the Arduino
	get_dotsEntry()	#Gets the number of dots from the dots entry window
	get_rastersEntry()	#Gets the number of rasters from the raster entry window
	ser.write('r' + dots + rasters)	#Sends the raster string to the Arduino
	tempHumidityFile.write("Raster started\n")
	
#Sending a DC raster command to the Arduino
def sendDCRaster():
	global dcRasterLength
	global dcRasterPitch
	global rasterRunning
	rasterRunning = True
	get_highVoltageEntry()	#Sends current value in high voltage entry window to the Arduino
	get_lowVoltageEntry()	#Sends current value in low voltage entry window to the Arduino
	get_dcRasterLengthEntry()	#Sends current value in DC X Raster Length entry window to the Arduino
	get_dcRasterPitchEntry()	#Sends current value in the DC Y Raster Pitch entry window to the Arduino
	get_rastersEntry()	#Gets the number of rasters from the raster entry window
	ser.write('f' + rasters)	#Sends the DCraster string to the Arduino

	
#Updating coordinate changes that occur during raster process
def rasterCoordinateUpdate():
	global xcoor
	global ycoor
	global xpitch
	global ypitch
	global rasterCoor
	global rasterRunning
	if(rasterRunning):	#Checks if the sendRaster function is currently running
		testRasterCoor = ser.readline()	#Reads a line from the serial input
		if(len(testRasterCoor)==0):	#If the line read is empty, it assigns a dummy value to the trigger character
			rasterCoor = '@'
		else:	#If the value is not empty, it assigns the first character read from the serial line to the trigger character
			rasterCoor = testRasterCoor[0]
		print(rasterCoor)
		if(rasterCoor == '^'):	#Increments the y coordinate when the corresponding trigger character is read
			ycoor = ycoor + ypitch
			ycoorEntry.delete(0,END)
			ycoorEntry.insert(10, '{:+.3f}'.format(ycoor))
		elif(rasterCoor == '%'):	#Decrements the x coordinate when the corresponding trigger character is read
			xcoor = xcoor - xpitch
			xcoorEntry.delete(0,END)
			xcoorEntry.insert(10, '{:+.3f}'.format(xcoor))
		elif(rasterCoor == '$'):	#Increments the x coordinate when the corresponding trigger character is read
			xcoor = xcoor + xpitch
			xcoorEntry.delete(0,END)
			xcoorEntry.insert(10, '{:+.3f}'.format(xcoor))
		elif(rasterCoor == '&'):	#Stops trying to read values from the serial input when the raster is done ('&' is sent from the Arduino when the raster is done)
			rasterCoor = '@'	#Assigns a dummy value to the trigger character
			tempHumidityFile.write("Raster completed\n")
			rasterRunning = False
	window.after(10, rasterCoordinateUpdate)	#The GUI will run this function every 10ms
	
def browseForFile(*event):
	from tkFileDialog import askopenfilename
	file = askopenfilename()
	fileNameEntry.delete(0,END)
	fileNameEntry.insert(0,file)

#Runs a file entered into the file entry in the GUI
def get_fileNameEntry(*event):
	global fileName
	global functionRunning
	global fileInProcess
	checkFunctionCompletion() #Checks to see if the arduino is busy before it sends a file
	if not functionRunning:
		functionRunning = True
		fileInProcess = True
		fileName = fileNameEntry.get()
		try:
			f = open(fileName,'r')
			numLines = file_len(f)
			f.seek(0)
			execute_File(f,numLines)
		except IOError:
			print(fileName + " does not exist in this directory")
			functionRunning = False
			fileInProcess = False

#Counts the number of lines of code in a file
def file_len(f):
    for i, l in enumerate(f):
		pass
    return i + 1

#Sends file commands to the arduino in groups of lines at a time. Do not try to send an entire file at one time or the arduino serial buffer will flood
def execute_File(f,numLines):
	global function
	global fileInProcess
	tempHumidityFile.write(fileName + " started\n")
	if(numLines % 40 != 0):	#Executes a file that does not have a multiple of 40 lines
		for i in range(0,numLines/40):	#Sends 40 lines of code
			for j in range(0,40):
				parseLine(f)
			function = function + "~"	#Tells the arduino that the code is not done sending
			ser.write(function)
			function = "";
			while(fileInProcess):	#Waits until the arduino processes previous 40 lines before sending more code
				functionRunningRead = ser.readline()
				print(functionRunningRead)
				try:
					if functionRunningRead[0] == "?":
						fileInProcess = False
					else:
						sleep(.001)
				except IndexError:
					sleep(.001)
		for i in range(0,numLines % 40):	#Sends last few lines of code
			parseLine(f)
	elif(numLines % 39 != 0):	#Executes a file that does not have a multiple of 39 lines
		for i in range(0,numLines/39):	#Sends 39 lines of code
			for j in range(0,39):
				parseLine(f)
			function = function + "~"	#Tells the arduino that the code is not done sending
			ser.write(function)
			print(function)
			function = "";
			while(fileInProcess):	#Waits until the arduino processes previous 39 lines before sending more code
				functionRunningRead = ser.readline()
				try:
					if functionRunningRead[0] == "?":
						fileInProcess = False
					else:
						sleep(.001)
				except IndexError:
					sleep(.001)
		for i in range(0,numLines % 39):	#Sends last few lines of code
			parseLine(f)
	tempHumidityFile.write(fileName + " completed\n")

#Translates a file in pseudo-aerotech to executable arduino commands
def parseLine(f):
	global function
	global timeType
	global generatedFile
	line = f.readline()
	# strip comments:
	bits = line.split(';',1)
	if (len(bits) > 1):
		comment = bits[1]
	# extract & clean command
	command = bits[0].strip()
	# code is first word, then args
	comm = command.split(None, 1)
	code = comm[0] if (len(comm)>0) else None
	args = comm[1] if (len(comm)>1) else None
	#if args:
		#args = args.replace(" ","")
	if code== "G1" or code == "LINEAR" or code == "RAPID":
		#xyzuDistance = 0;
		copyArgs = args;
		args = args.replace(" ","")
		function = function + "l" + args + "s"
		#ser.write("l"+args+"s")
		#copyArgs = copyArgs.replace("x","")
		#copyArgs = copyArgs.replace("y","")
		#copyArgs = copyArgs.replace("z","")
		#copyArgs = copyArgs.replace("u","")
		#argsComponents = copyArgs.split(' ')
		#for i in range(0,len(argsComponents)):
			#argsComponents[i]= float(argsComponents[i])
			#xyzuDistance = xyzuDistance + abs(argsComponents[i])
		#sleep(.005*xyzuDistance)
	elif code == "PULSE":
		function = function + "e"
	elif code == "G4" or code == "DWELL":	#This has resolution up to 1ms
		if timeType:	#Input is in seconds. (This is assumed unless MINUTES is explicitly called in the file
			args = float(args)*1000
			args = long(args)
			function = function + "d" + str(args)
		else:	#Input is in minutes
			args = float(args)*60000
			args = long(args)
			function = function + "d" + str(args)
	elif code == "G75" or code == "MINUTES":
		timeType = False
	elif code == "G76" or code == "SECONDS":
		timeType = True
	elif code == "G92" or code =="POSOFFSET":
		do_G92(args)
		print(args)
	elif code == "VOLTAGEHIGH":	#Voltage is the voltage at the nozzle
		print("vh" + args)
		function = function + "vh" + args
	elif code == "VOLTAGELOW":	#Voltage is the voltage at the nozzle
		print("vl"+args)
		function = function + "vl" + args
	elif code == "TIMEHIGH":
		if timeType:	#Input is in seconds. (This is assumed unless MINUTES is explicitly called in the file
			args = float(args)*1000
			args = long(args)
			function = function + "th" + str(args)
		else:	#Input is in minutes
			args = float(args)*60000
			args = long(args)
			function = function + "th" + str(args)
	elif code == "TIMELOW":
		if timeType:	#Input is in seconds. (This is assumed unless MINUTES is explicitly called in the file
			args = float(args)*1000
			args = long(args)
			function = function + "tl" + str(args)
		else:	#Input is in minutes
			args = float(args)*60000
			args = long(args)
			function = function + "tl" + str(args)
	elif code == "END":	#Signals the end of the file and sends the function to the arduino. All files sent should end with the END command
		function = function + "!"
		print function
		ser.write(function)
		function = ""
		
#Sets the coordinate system to a desired value
def do_G92(args):
	global xcoor
	global ycoor
	global zcoor
	#global ucoor #Removed this line for printer D
	#global ztotcoor #Removed this line for printer D
	argsComponents = args.split(' ')
	for i in range(0,len(argsComponents)):
		if argsComponents[i][0] == 'X' or argsComponents[i][0] == 'x':
			argsComponents[i] = argsComponents[i][1:]
			xcoor = float(argsComponents[i])
			xcoorEntry.delete(0,END)
			xcoorEntry.insert(10, '{:+.3f}'.format(xcoor))
		elif argsComponents[i][0] == 'Y' or argsComponents[i][0] == 'y':
			argsComponents[i] = argsComponents[i][1:]
			ycoor = float(argsComponents[i])
			ycoorEntry.delete(0,END)
			ycoorEntry.insert(10, '{:+.3f}'.format(ycoor))
		elif argsComponents[i][0] == 'Z' or argsComponents[i][0] == 'z':
			argsComponents[i] = argsComponents[i][1:]
			zcoor = float(argsComponents[i])
			zcoorEntry.delete(0,END)
			zcoorEntry.insert(10, '{:+.3f}'.format(zcoor))
		#Removed this section for printer D
			#Resets the total vertical value. Check and see how people would prefer to do this. (If setting Z should set the total value = z, or if the old u value should be included as well)
			# ucoor=0
			# ztotcoor = zcoor + ucoor
			# ztotcoorEntry.delete(0,END)
			# ztotcoorEntry.insert(10, '{:+.3f}'.format(ztotcoor))
		# elif argsComponents[i][0] == 'U' or argsComponents[i][0] == 'u':
			# argsComponents[i] = argsComponents[i][1:]
			# ucoor = float(argsComponents[i])
			# ucoorEntry.delete(0,END)
			# ucoorEntry.insert(10, '{:+.3f}'.format(ucoor))
			#Resets the total vertical value. Check and see how people would prefer to do this. (If setting U should set the total value = U, or if the old z value should be included as well)
			# zcoor = 0
			# ztotcoor = zcoor + ucoor
			# ztotcoorEntry.delete(0,END)
			# ztotcoorEntry.insert(10, '{:+.3f}'.format(ztotcoor))
			
#Prevents a file to be sent to the arduino until the arduino is done running a function
def checkFunctionCompletion():
	global functionRunning
	if(functionRunning):
		functionRunningRead = ser.readline()
		functionRunningRead.strip()
		print(functionRunningRead)
		try:
			if functionRunningRead[0] == "!":
				functionRunning = False
		except IndexError:
			print("Arduino is currently busy")

#Writes temperature and humidity data from the Arduino Uno to a file every 15 seconds	
def tempHumidityFileWrite():
	global tempHumiditySerial
	clock = datetime.datetime.now()
	time = "%d:%d:%d" % (clock.hour, clock.minute, clock.second)
	tempHumidityFile.write(time)
	data = tempHumiditySerial.readline()
	tempHumidityFile.write(data)
	window.after(15000,tempHumidityFileWrite)

#Writes the first temperature and humidity data to the file
if(UnoConnect):
	clock = datetime.datetime.now()
	time = "%d:%d:%d" % (clock.hour, clock.minute, clock.second)
	tempHumidityFile.write(time)
	data = tempHumiditySerial.readline()
	tempHumidityFile.write(data)
	
window = Tkinter.Tk()

window.after(10,rasterCoordinateUpdate)	#Runs the rasterCoordinateUpdate function every 10ms
if(UnoConnect):
	window.after(15000,tempHumidityFileWrite)

#Creating and positioning labels for the different variables
Label(window, text ="Jog X (mm):").grid(row=0)
Label(window, text ="Jog Y (mm):").grid(row=1)
Label(window, text ="Jog Z (mm):").grid(row=2)
#Label(window, text ="Jog U:").grid(row=3) #Removed this line for printer D
Label(window, text = "High Voltage:").grid(row=0, column = 4)
Label(window, text = "Low Voltage:").grid(row=1, column = 4)
Label(window, text = "Pulse ON Time:").grid(row=2, column = 4)
Label(window, text = "Pulse OFF Time:").grid(row=3, column = 4)
Label(window, text = "Motor Speed Delay (ms):").grid(row=4, column = 4)
Label(window, text ="	").grid(row=4)
Label(window, text ="	").grid(row=5)
Label(window, text ="	").grid(row=6)
Label(window, text ="X Pitch:").grid(row=7)
Label(window, text ="Y Pitch:").grid(row=8)
Label(window, text = "DC X Raster Length:").grid(row=9)
Label(window, text = "DC Y Raster Pitch:").grid(row=10)
Label(window, text = "# of Dots:").grid(row=7, column = 4)
Label(window, text = "# of Rasters:").grid(row=8, column = 4)
Label(window, text = "	").grid(row = 0, column = 7)
Label(window, text = "	").grid(row = 0, column = 8)
Label(window, text = "Set X Location:").grid(row = 11)
Label(window, text = "Set Y Location:").grid(row = 12)
Label(window, text = "Set Z Location:").grid(row = 13)
#Label(window, text = "U Location:").grid(row = 3, column = 9) #Removed this line for printer D
#Label(window,text = "Vertical Location (Z+U):").grid(row=4,column=9) #Removed this line for printer D
Label(window, text = "X Position").grid(row = 0, column = 9)
Label(window, text = "Y Position").grid(row = 1, column =9)
Label(window, text = "Z Position").grid(row = 2, column =9)

Label(window, text = "	").grid(row = 0, column = 11)
Label(window, text = "Executable File:").grid(row=7, column = 9)


#Creating an entry window for the user to input values
xjogentry = Entry(window)
yjogentry = Entry(window)
zjogentry = Entry(window)

#ujogentry = Entry(window) #Removed this line for printer D
highVoltageEntry = Entry(window)
lowVoltageEntry = Entry(window)
onTimeEntry = Entry(window)
offTimeEntry = Entry(window)
stepDelayEntry = Entry(window)
xPitchEntry = Entry(window)
yPitchEntry = Entry(window)
dotsEntry = Entry(window)
rastersEntry = Entry(window)
dcRasterLengthEntry = Entry(window)
dcRasterPitchEntry = Entry(window)

#Creating an entry window for showing current coordinates
xcoorEntry = Entry(window)
ycoorEntry = Entry(window)
zcoorEntry = Entry(window)
#ucoorEntry = Entry(window) #Removed this line for printer D
#ztotcoorEntry = Entry(window) #Removed this line for printer D

#Creating an entry window for setting desired coordinates
newxcoorEntry = Entry(window)
newycoorEntry = Entry(window)
newzcoorEntry = Entry(window)
#newucoorEntry = Entry(window) #Removed this line for printer D

#Creating an entry window for inputting G code file
fileNameEntry = Entry(window)

#Positioning the entry windows
xjogentry.grid(row=0,column=1)
yjogentry.grid(row=1,column=1)
zjogentry.grid(row=2,column=1)
#ujogentry.grid(row=3,column=1) #Removed this line for printer D
highVoltageEntry.grid(row=0,column=5)
lowVoltageEntry.grid(row=1,column=5)
onTimeEntry.grid(row=2,column=5)
offTimeEntry.grid(row=3,column=5)
stepDelayEntry.grid(row=4,column=5)
xPitchEntry.grid(row=7,column=1)
yPitchEntry.grid(row=8,column=1)
dotsEntry.grid(row=7,column=5)
rastersEntry.grid(row=8,column=5)
xcoorEntry.grid(row=0,column=8)
ycoorEntry.grid(row=1,column=8)
zcoorEntry.grid(row=2,column=8)
#ucoorEntry.grid(row=3,column=10) #Removed this line for printer D
#ztotcoorEntry.grid(row=4,column=10) #Removed this line for printer D
newxcoorEntry.grid(row=11,column=1)
newycoorEntry.grid(row=12,column=1)
newzcoorEntry.grid(row=13,column=1)

#newucoorEntry.grid(row=3,column=12) #
fileNameEntry.grid(row = 7, column = 10)
dcRasterLengthEntry.grid(row = 9, column = 1)
dcRasterPitchEntry.grid(row = 10, column = 1)

#Triggers the button corresponding to the entry box that the cursor is currently in
xjogentry.bind('<Return>', get_xjogentry)
yjogentry.bind('<Return>',get_yjogentry)
zjogentry.bind('<Return>',get_zjogentry)
#ujogentry.bind('<Return>',get_ujogentry) #Removed this line for printer D
highVoltageEntry.bind('<Return>',get_highVoltageEntry)
lowVoltageEntry.bind('<Return>',get_lowVoltageEntry)
onTimeEntry.bind('<Return>',get_onTimeEntry)
offTimeEntry.bind('<Return>',get_offTimeEntry)
stepDelayEntry.bind('<Return>',get_stepDelayEntry)
newxcoorEntry.bind('<Return>',get_newxcoorEntry)
newycoorEntry.bind('<Return>',get_newycoorEntry)
newzcoorEntry.bind('<Return>',get_newzcoorEntry)
#newucoorEntry.bind('<Return>',get_newucoorEntry) #Removed this line for printer D
xPitchEntry.bind('<Return>',get_xPitchEntry)
yPitchEntry.bind('<Return>',get_yPitchEntry)
dotsEntry.bind('<Return>',get_dotsEntry)
rastersEntry.bind('<Return>',get_rastersEntry)
fileNameEntry.bind('<Return>',get_fileNameEntry)
dcRasterLengthEntry.bind('<Return>',get_dcRasterLengthEntry)
dcRasterPitchEntry.bind('<Return>',get_dcRasterPitchEntry)

#Creating and positioning buttons to enter the inputted values from the entry window to the output functions
Button(window, text='Enter X Jog', command =lambda: get_xjogentry()).grid(row=0,column=2,sticky = W, pady=4)
Button(window, text='Enter Y Jog', command =lambda: get_yjogentry()).grid(row=1,column=2,sticky = W, pady=4)
Button(window, text='Enter Z Jog', command =lambda: get_zjogentry()).grid(row=2,column=2,sticky = W, pady=4)
Button(window, text='Reset Origin', command =lambda: reset_origin()).grid(row=14,sticky = W, pady=4)
#Button(window, text='Enter U Jog', command =lambda: get_ujogentry()).grid(row=3,column=2,sticky = W, pady=4) #Removed this line for printer D
Button(window, text='Enter High Voltage', command =get_highVoltageEntry).grid(row=0,column=6,sticky = W, pady=4)
Button(window, text='Enter Low Voltage', command =get_lowVoltageEntry).grid(row=1,column=6,sticky = W, pady=4)
Button(window, text='Enter ON Time', command =get_onTimeEntry).grid(row=2,column=6,sticky = W, pady=4)
Button(window, text='Enter OFF Time', command =get_offTimeEntry).grid(row=3,column=6,sticky = W, pady=4)
Button(window, text='Enter Motor Speed Delay', command =get_stepDelayEntry).grid(row=4,column=6,sticky = W, pady=4)
Button(window, text='Reset to New Coordinates', command =lambda: get_newCoordinatesEntry()).grid(row=4,column=12,sticky = W, pady=4)
Button(window, text='Send Raster', command =lambda: sendRaster()).grid(row=7, column=8,sticky=W,pady=4);
Button(window, text = 'Browse', command = lambda: browseForFile()).grid(row=7, column = 11, sticky=W,pady=4)
Button(window, text='Read File', command =lambda: get_fileNameEntry()).grid(row=7, column=12,sticky=W,pady=4);
Button(window, text='Send DC Raster', command =lambda: sendDCRaster()).grid(row=8, column=8,sticky=W,pady=4);
Button(window, text='Cure Light On/Off', command =lambda: light_switch()).grid(row=9, column=8,sticky=W,pady=4);
Button(window, text='Turn on High Voltage', command =lambda: turnOnHighVoltage()).grid(row=9, column=5,sticky=W,pady=4);
Button(window, text='Turn on Low Voltage', command =lambda: turnOnLowVoltage()).grid(row=10, column=5,sticky=W,pady=4);

window.mainloop()
