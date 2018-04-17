import socket
from time import sleep
with socket.socket() as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('172.27.76.59', 8765))
    sock.listen(1)
    conn, addr = sock.accept()
    conn.settimeout(10)
    while True:
        data = conn.recv(1024)
        print(data.split())