import struct, random, sys
from socket import socket, AF_INET, SOCK_STREAM
from select import select

hostname, port = sys.argv[1], sys.argv[2]
server_addr = (hostname, int(port))

def valuateResoult(num, operator, guess):
    if operator == '=':
        return 'Y' if num == guess else 'K'
    elif operator == '<' or operator == '>':
        return 'I' if eval(str(num)+operator+str(guess)) else 'N'
    else:
        return 'E'

num = random.randint(0,100)
packer = struct.Struct("c i")

with socket(AF_INET, SOCK_STREAM) as server:
    inputs = [ server ]
    server.bind(server_addr)
    server.listen(5)
    
    while True:
        timeout = 1
        r, w, e = select(inputs,inputs,inputs,timeout)
        
        if not (r or w or e):
            continue
        
        for s in r:
            if s is server:
                client, client_addr = s.accept()
                inputs.append(client)
            else:
                data = s.recv(packer.size)
                if not data:
                    inputs.remove(s)
                    s.close()
                else:
                    operator, guess = packer.unpack(data)
                    operator = operator.decode()
                    result = valuateResoult(num, operator, guess)
                    response = packer.pack(result.encode(),0)
                    s.sendall(response)
                    if result == 'Y':
                        print(client_addr," guessed the correct solution: ",num)
                        for client_socket in inputs:
                            if client_socket is not server:
                                try:
                                    client_socket.sendall(packer.pack('V'.encode(),0))
                                    num = random.randint(0,100)
                                except:
                                    print("Error sending message to ",client_socket)