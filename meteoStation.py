import os
import datetime
import socket
from time import sleep, time

#file.write('Flux Humidity SkyT infraredT outsideT\n')
def open_connection():
	sock = socket.socket()
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('172.27.76.59', 8765))
	#print('bind OK')
	sock.listen(1)
	print('Waiting signal from the meteo station...')
	conn, addr = sock.accept()
	#print('listen')
	conn.settimeout(100)
	print('conn OK')
	return conn

def read_meteoData(conn):
	data = conn.recv(256).split()
	#print(data)
	if len(data) == 6:
		if data[0] == '0.00':
		    print('Troyka sensor return 0.00')
		    return False
		data[0] = '%.2f' % float(data[0])
		data[1] = '%.2f' % float(data[1])
		data[2] = '%.2f' % float(data[2])
		data[3] = '%.2f' % float(data[3])
		data[4] = '%.2f' % float(data[4])
		data[5] = '%.2f' % float(data[5])
	else:
		return False
	return data

def main():
	conn = open_connection()
	while True:
		#print('Waiting for the data...')
		data = read_meteoData(conn)
		if data:
			f = open('data.txt', 'a')
			t = datetime.datetime.now()
			line = t.strftime("%Y-%m-%d %H:%M:%S")+' '+' '.join(data)+'\n'
			f.writelines(line)
			f.flush()
			f.close()
			print(line)
		sleep(1)

if __name__ == "__main__":
	main()