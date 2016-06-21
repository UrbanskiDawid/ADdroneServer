import socket
import time
import datetime
 
UDP_IP = '52.58.5.47'
UDP_PORT = 5005
 
print "Ping test - Client" 
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
                     
print "Starting..."

counter = 0
summ = 0 
                  
while 1:                
    sock.sendto('%%%%', (UDP_IP, UDP_PORT))
    pingTimestamp = datetime.datetime.now()
    pongReceived = False
    while not pongReceived:
        data, addr = sock.recvfrom(1024)
        if '%%%%' in data:
            now = datetime.datetime.now()
            pongReceived = True
            counter += 1
            d = now - pingTimestamp
            milis = (d.seconds*1000.0 + d.microseconds/1000.0)/2.0
            summ += milis
                        
            print ' <UDP> Ping:', milis, 'ms\tmean:', (summ/counter), 'ms'
    time.sleep(2.0)

print 'DONE'
