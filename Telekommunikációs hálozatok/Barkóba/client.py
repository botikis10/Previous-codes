import sys, time, struct, random, math
from socket import socket, AF_INET, SOCK_STREAM
from select import select

hostname, port = sys.argv[1], sys.argv[2]
server_addr = (hostname, int(port))

min = 0
max = 99

packer = struct.Struct("c i")

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    while min < max+1:
        time.sleep(random.randint(1,5))
        guess = math.floor((min+max)/2)
        print("Guessing: ",guess)
        data = packer.pack('<'.encode(),guess)
        client.sendall(data)
        result = client.recv(packer.size)
        unpacked_result = packer.unpack(result)
        if unpacked_result[0].decode() == 'I':
            max = guess-1
        elif unpacked_result[0].decode() == 'N':
            min = guess+1
        elif unpacked_result[0].decode() == 'V':
            sys.exit()
            
    guess = min
    print("Guessing: ",guess)
    data = packer.pack('>'.encode(),guess)
    client.sendall(data)
    result = client.recv(packer.size)
    unpacked_result = packer.unpack(result)
    if unpacked_result[0].decode() == 'I':
        max = guess-1
    elif unpacked_result[0].decode() == 'N':
        guess = max
        print("Solution: ",guess)
        data = packer.pack('='.encode(),guess)
        client.sendall(data)
        result = client.recv(packer.size)
        unpacked_result = packer.unpack(result)
        print(unpacked_result[0].decode())
    result = client.recv(packer.size)
    unpacked_result = packer.unpack(result)
    print(unpacked_result[0].decode())
    if unpacked_result[0].decode() == 'V':
        #client.diconnect
        pass
