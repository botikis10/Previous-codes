from sys import argv, exit
import socket, zlib

# python netcopy_cli.py localhost 50000 localhost 50001 01 lorem.txt

if len(argv) < 7:
	print("Invalid argument list")
	exit()

server_conn = socket.socket()
server_conn.connect((argv[1], int(argv[2])))

proxy_conn = socket.socket()
proxy_conn.connect((argv[3], int(argv[4])))

with open(argv[6], 'rb') as f:
	data = f.read(1024)
	crcvalue = 0
	while data:
		server_conn.send(data)
		crcvalue = zlib.crc32(data, crcvalue)
		data = f.read(1024)
server_conn.close()

crc = str(crcvalue)
msg = ('BE|' + argv[5] + '|60|' + str(len(crc)) + '|' + crc).encode('utf-8')
proxy_conn.sendall(msg)
data = proxy_conn.recv(1024)
print(data)
