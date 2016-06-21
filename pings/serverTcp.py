import socket
import sys
import time

TCP_IP = 'localhost'
TCP_PORT = 6666

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

print "Starting TCP ping server..."

while True:
    connection, address = sock.accept()
    print 'User connected!, @ ', address
    adr = address
    break
 
flag = True
while True:
    try:
        data = connection.recv(1024) # buffer size is 1024 bytes
        if '%%%%' in data:
            connection.send('%%%%')
            if flag:
                sys.stdout.write("\rProcessing /")
                sys.stdout.flush()
                flag = False
            else:
                sys.stdout.write("\rProcessing \\")
                sys.stdout.flush()
                flag = True
            
    except:
        print 'Client disconected'
        break
        
print 'exiting'
sock.close()
