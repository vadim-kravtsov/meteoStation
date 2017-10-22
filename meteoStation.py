import serial
from Tkinter import *
import tkFont
from time import sleep
import threading
import os

if os.name == 'nt':
	ser = serial.Serial('COM3', baudrate = 9600, timeout = 1)
else:
	ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)
	
data = ser.readline().split()

root = Tk()
try:
	helv14 = tkFont.Font(family="Helvetica",size=14)
except:
	helv14 = tkFont.Font(family="Arial",size=14)
t = StringVar()
p = StringVar()
h = StringVar()
#this gets called every 10 ms
def periodically_called():
	while True:
		sleep(1)
		data = ser.readline().split()
		if len(data) == 3:
			data[0] = '%.1f' % float(data[0])
			data[1] = '%.0f' % float(data[1])
			data[2] = '%.1f' % float(data[2])
			t.set('Temperature:\n'+data[0]+' *C')
			p.set('Pressure:\n'+data[1]+' mmHg')
			h.set('Humidity:\n'+data[2]+' %')

thread = threading.Thread(target=periodically_called)
thread.daemon = True 
thread.start()
	
tLabel = Label(root,textvariable=t, bg = '#edeff2', fg = '#1e2530', font=helv14)
pLabel = Label(root,textvariable=p, bg = '#edeff2', fg = '#1e2530', font=helv14)
hLabel = Label(root,textvariable=h, bg = '#edeff2', fg = '#1e2530', font=helv14)

tLabel.pack(fill = X, expand = True)
pLabel.pack(fill = X, expand = True)
hLabel.pack(fill = X, expand = True)

root.title('meteoData')
root.geometry("180x200")
root.configure(background='#edeff2')
root.mainloop()