import serial
from Tkinter import *
import tkFont
from time import sleep, time
import threading
import os

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
D = [[],[]]

def periodically_called():
	i=0
	k=0
	fig = Figure()
	a = fig.add_subplot(111)
	a.set_title('Humidity')
	a.set_xlabel('time')
	a.set_ylabel('H, %')
	a.grid(True)
	canvas = FigureCanvasTkAgg(fig, master = root)
	canvas.get_tk_widget().pack(fill = X, expand = True)
		
	while True:
		sleep(1)
		data = ser.readline().split()
		if len(data) == 3:
			data[0] = '%.1f' % float(data[0])
			data[1] = '%.0f' % float(data[1])
			data[2] = '%.2f' % float(data[2])
			t.set('Temperature:\n'+data[0]+' *C')
			p.set('Pressure:\n'+data[1]+' mmHg')
			h.set('Humidity:\n'+data[2]+' %')
			if i==2:
				D[0].append(k)
				D[1].append(float(data[2]))
				a.ylim = [min(D[1]), max(D[1])] 
				a.plot(D[0],D[1],color='blue')
				canvas.draw()
				i=0
			i=i+1
			k+=1




thread = threading.Thread(target=periodically_called)
thread.daemon = True 
thread.start()
	
tLabel = Label(root,textvariable=t, bg = '#edeff2', fg = '#1e2530', font=helv14)
pLabel = Label(root,textvariable=p, bg = '#edeff2', fg = '#1e2530', font=helv14)
hLabel = Label(root,textvariable=h, bg = '#edeff2', fg = '#1e2530', font=helv14)

tLabel.pack(fill = Y, expand = True)
pLabel.pack(fill = Y, expand = True)
hLabel.pack(fill = Y, expand = True)

root.title('meteoData')
root.geometry("500x500")
root.configure(background='#edeff2')
root.mainloop()