import socket
import sys
import time

UDP_IP = 'localhost'
UDP_PORT = 8080 # ??????
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

print 'Server started over UDP, adr: ', UDP_IP, ':', UDP_PORT
 
flag = True
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if '%%%%' in data:
        sock.sendto('%%%%', addr)
        if flag:
            sys.stdout.write("\rProcessing /")
            sys.stdout.flush()
            flag = False
        else:
            sys.stdout.write("\rProcessing \\")
            sys.stdout.flush()
            flag = True
