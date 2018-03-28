import os
import datetime
import socket
from time import sleep, time

file = open('data.txt', 'a')
#file.write('Flux Humidity SkyT AmbientT InsideT\n')
def open_connection():
	sock = socket.socket()
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('172.27.76.59', 8765))
	sock.listen(1)
	conn, addr = sock.accept()
	conn.settimeout(100)
	return conn

def read_meteoData(conn):
	data = conn.recv(256).split()
	print(data)
	if len(data) == 5:
		data[0] = '%.2f' % float(data[0])
		data[1] = '%.2f' % float(data[1])
		data[2] = '%.2f' % float(data[2])
		data[3] = '%.2f' % float(data[3])
		data[4] = '%.2f' % float(data[4])
	else:
		return False
	return data

def main():
	conn = open_connection()
	while True:
		data = read_meteoData(conn)
		if data:
			t = datetime.datetime.now()
			file.writelines(t.strftime("%Y-%m-%d %H:%M:%S")+' '+' '.join(data)+'\n')
		else:
			print("Wait...")
		file.flush()
		sleep(1)

if __name__ == "__main__":
	main()