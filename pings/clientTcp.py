import socket
import sys
import time
import select
import datetime

TCP_IP = '52.58.5.47'
TCP_PORT = 6666

print "Ping test - Client" 
print "TCP target IP:", TCP_IP
print "TCP target port:", TCP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((TCP_IP, TCP_PORT))
except:
    print 'Unable to connect'
    sys.exit()

counter = 0
summ = 0 
                  
while 1:    
    sock.send('%%%%')
    pingTimestamp = datetime.datetime.now()
    pongReceived = False
    while not pongReceived:
        data = sock.recv(1024)
        if '%%%%' in data:
            now = datetime.datetime.now()
            pongReceived = True
            counter += 1
            d = now - pingTimestamp
            milis = (d.seconds*1000.0 + d.microseconds/1000.0)/2.0
            summ += milis
                        
            print ' <TCP> Ping:', milis, 'ms\tmean:', (summ/counter), 'ms'
    time.sleep(2.0)

print 'DONE'
