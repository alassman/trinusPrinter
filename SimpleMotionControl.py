import serial
import Tkinter
import time
import datetime
import math

from Tkinter import *
from time import sleep

initialStepDelay = 37

#Connecting to the Arduino at a baudrate of 115200
try:
    ser = serial.Serial('COM7',115200,timeout = 2)
    print("Connection to motor/voltage Arduino Mega successful\n")
    print("Initialize Step Delay to " + str(initialStepDelay))
    ser.write('s' + str(initialStepDelay))
    print("motor speed set")
except Exception as e:
    print(e)
try:
    tempHumiditySerial = serial.Serial('COM5',9600,timeout = 2)
    print("Connection to sensor Arduino Uno successful\n")
    UnoConnect = True
except Exception as e:
    print(e)
    UnoConnect = False
    
Positive = "Positive"
Negative = "Negative"
xcoor = 0.0
ycoor = 0.0
zcoor = 0.0
mmToJogDist = 118.75
JogDistTomm = 0.00842105263157895

#Creating file for recording temperature and humidity
tempHumidityFile = open('Temperature Humidity Data.txt','w')
tempHumidityFile.write("Time    Humidity    Temperature\n")

# TODO:
# Measure ratio between steps and millimeters on printer
# attempt to receive feedback from arduino - so that we know when it completes a jog command
# Each marking is one milimeter

#Sending the desired jog distance to the Arduino. Have to write in how to convert from distance to # of steps
def get_xjogentry(direction=None, event = None):
    try:
        getAndSet_stepDelayEntry()
        distance = float(xjogentry.get()) 
        if direction != "Enter" and direction == Negative:
            distance = distance * -1
        print (direction)
        ser.write('x' + str(int(distance * mmToJogDist)))
        print('x' + str(int(distance * mmToJogDist)))
        set_xcoor(distance)
    except:
        messageWindow.delete(0, END)
        messageWindow.insert(0, "Please Enter a X Jog Value")

def get_yjogentry(direction=None, event=None):
    try:
        getAndSet_stepDelayEntry()
        distance = float(yjogentry.get()) 
        if direction != "Enter" and direction == Negative:
            distance = distance * -1
        ser.write('y' + str(int(distance * mmToJogDist)))
        print('y' + str(int(distance * mmToJogDist)))
        set_ycoor(distance)
    except:
        messageWindow.delete(0, END)
        messageWindow.insert(0, "Please Enter a Y Jog Value")


def get_zjogentry(direction=None, event=None):
    try:
        getAndSet_stepDelayEntry()
        distance = float(zjogentry.get()) 
        if direction != "Enter" and direction == Negative:
            distance = distance * -1
        ser.write('z' + str(int(distance * mmToJogDist)))
        print('z' + str(int(distance * mmToJogDist)))
        set_zcoor(distance)
    except:
        messageWindow.delete(0, END)
        messageWindow.insert(0, "Please Enter a Z Jog Value")


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
    
#Outputting the current coordinate system
def set_xcoor(distance, event=None):
    global xcoor
    xcoor = xcoor + distance
    xcoorEntry.delete(0,END)
    xcoorEntry.insert(10, '{:+.3f}'.format(xcoor))
    
def set_ycoor(distance, event=None):
    global ycoor
    ycoor = ycoor + distance
    ycoorEntry.delete(0,END)
    ycoorEntry.insert(10, '{:+.3f}'.format(ycoor))
    
def set_zcoor(distance, event=None):
    global zcoor
    zcoor = zcoor + distance
    zcoorEntry.delete(0,END)
    zcoorEntry.insert(10, '{:+.3f}'.format(zcoor))

#Sending the delay between steps to the Arduino
def getAndSet_stepDelayEntry(*event):
    print("Step Delay time: " + str(motorSpeedSlider.get()))
    ser.write('s' + str(motorSpeedSlider.get()))
    #print("send: " + str(motorSpeedSlider.get()))
    print("motor speed set")

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

# window.after(10,rasterCoordinateUpdate)   #Runs the rasterCoordinateUpdate function every 10ms
if(UnoConnect):
    window.after(15000,tempHumidityFileWrite)

#Creating and positioning labels for the different variables
Label(window, text ="Jog X (mm):").grid(row=0)
Label(window, text ="Jog Y (mm):").grid(row=1)
Label(window, text ="Jog Z (mm):").grid(row=2)
Label(window, text = "X Position").grid(row = 4)
Label(window, text = "Y Position").grid(row = 5)
Label(window, text = "Z Position").grid(row = 6)
Label(window, text = "Z Position").grid(row = 6)
Label(window, text = "Fast\t\t\tSlow").grid(row = 8, column=1)
Label(window, text = "  ").grid(row = 0, column = 11)

# Function to clean "trash" entry widget
def emptyTrash(event=None):
    trash.delete(0, END)
    trash.insert(0, "Click here to use keys")

# Create key press event bindings
BACK = "b"
FORWARD = "f"
LEFT = "l"
RIGHT = "r"
UP = "u"
DOWN = "d"
QUIT = "q"
RESET = "o"

def key(event):
    # print (event.char)
    if event.char == FORWARD:
        print("FORWARD")
        get_xjogentry(Negative)
    elif event.char == BACK:
        print("BACK")
        get_xjogentry(Positive)
    elif event.char == LEFT:
        print("LEFT")
        get_yjogentry(Negative)
    elif event.char == RIGHT:
        print("RIGHT")
        get_yjogentry(Positive)
    elif event.char == UP:
        print("UP")
        get_zjogentry(Positive)
    elif event.char == DOWN:
        print("DOWN")
        get_zjogentry(Negative)
    elif event.char == RESET:
        reset_origin()
    elif event.char == QUIT:
        print("GOOD BYE")
        window.quit()

    emptyTrash()


window.bind("<Key>", key)

#Creating an entry window for the user to input values
xjogentry = Entry(window)
yjogentry = Entry(window)
zjogentry = Entry(window)

#Creating an entry window for showing current coordinates
xcoorEntry = Entry(window)
ycoorEntry = Entry(window)
zcoorEntry = Entry(window)

# User must click in this window to be able to use keyboard keys
# when key is hit, the actual entry will be put in this window, 
# then immediatly overwritten by the function emptyTrash() called
# in the key() function
trash = Entry(window)
trash.insert(0, "Click here to use keys")

# Slider to set speed of motors
motorSpeedSlider = Scale(window, from_=33, to=49, length=250, label="Speed Controller", orient=HORIZONTAL)
motorSpeedSlider.set(initialStepDelay)

# Create Message window for user
messageWindow = Entry(window)
messageWindow.insert(0, "Have fun printing!")

#Positioning the entry windows
xjogentry.grid(row=0,column=1)
yjogentry.grid(row=1,column=1)
zjogentry.grid(row=2,column=1)
xcoorEntry.grid(row=4,column=1)
ycoorEntry.grid(row=5,column=1)
zcoorEntry.grid(row=6,column=1)
trash.grid(row=3)
messageWindow.grid(row=3,column=2)
motorSpeedSlider.grid(row=7,column=1)


#Triggers the button corresponding to the entry box that the cursor is currently in
xjogentry.bind('<Return>',get_xjogentry)
yjogentry.bind('<Return>',get_yjogentry)
zjogentry.bind('<Return>',get_zjogentry)

#Creating and positioning buttons to enter the inputted values from the entry window to the output functions
Button(window, text='Forward (f)', command =lambda: get_xjogentry(Positive)).grid(row=0,column=2,sticky = W, pady=4)
Button(window, text='Backward (b)', command =lambda: get_xjogentry(Negative)).grid(row=0,column=3,sticky = W, pady=4)

Button(window, text='Left (l)', command =lambda: get_yjogentry(Positive)).grid(row=1,column=2,sticky = W, pady=4)
Button(window, text='Right (r)', command =lambda: get_yjogentry(Negative)).grid(row=1,column=3,sticky = W, pady=4)

Button(window, text='Up (u)', command =lambda: get_zjogentry(Positive)).grid(row=2,column=2,sticky = W, pady=4)
Button(window, text='Down (d)', command =lambda: get_zjogentry(Negative)).grid(row=2,column=3,sticky = W, pady=4)

Button(window, text='Reset Origin (o)', command =lambda: reset_origin()).grid(row=4,column=2,sticky = W, pady=4)
Button(window, text='EXIT (q)', command =window.destroy).grid(row=7,column=0,sticky = W, pady=4)

window.mainloop()
