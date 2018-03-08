import serial
import os
from time import sleep, clock

file = open('data.txt', 'w')
file.write('Flux Humidity SkyT AmbientT InsideT\n')
def open_serial_port():
	if os.name == 'nt':
		ser = serial.Serial('COM3', baudrate = 9600, timeout = 1)
	else:
		ser = serial.Serial('/dev/ttyACM3', baudrate = 9600, timeout = 1)
	return ser

def read_meteoData(serialPort):
	ser = serialPort
	try:
		data = ser.readline().split()
		#print(data)
	except:
		return False
	if len(data) == 5:
		data[0] = '%.2f' % float(data[0])
		data[1] = '%.2f' % float(data[1])
		data[2] = '%.2f' % float(data[2])
		data[3] = '%.2f' % float(data[3])
		data[4] = '%.2f' % float(data[4])
	else:
		return False
	ser.reset_input_buffer()
	return data

def main():
	ser = open_serial_port()
	while True:
		data = read_meteoData(ser)
		if data:
			#pass
			file.writelines(str(clock())+' '+' '.join(data)+'\n')
		else:
			print("Wait...")
		sleep(1)

if __name__ == "__main__":
	main()