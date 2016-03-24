import serial

class UartSender:
    connection = None

    def __init__(self,device,baundRate):
        self.connection = serial.Serial(device)
        self.connection.baudrate = baundRate
        self.connection.timeout = 1        #non-block read
        self.connection.writeTimeout = 1   #timeout for write
        print ("UartSender constructed (", device, " at ",baundRate,")")

# OTHER OPTIONS
#        self.connection.bytesize = serial.EIGHTBITS #number of bits per bytes
#        self.connection.parity = serial.PARITY_NONE #set parity check: no parity
#        self.connection.stopbits = serial.STOPBITS_ONE #number of stop bits
#        self.connection.xonxoff = False     #disable software flow control
#        self.connection.rtscts = False     #disable hardware (RTS/CTS) flow control
#        self.connection.dsrdtr = False       #disable hardware (DSR/DTR) flow control

    def send(self, message):
        self.connection.write(message)

    def recv(self):
        data = None
        nbBytesWaitingInInputBuffer = self.connection.inWaiting()
        if nbBytesWaitingInInputBuffer > 0:
            try:
                data = self.connection.read(nbBytesWaitingInInputBuffer)
#                print("UART: received message ", str(data).rstrip() + "\n")
                # ans = self.connection.readline()   # read a '\n' terminated line
                # if not ans:
                #   raise  Error('no ans')
                # else:
                #   print 'UART: "',str(ans).rstrip(),'"'
            except:
                print('UART: read timeout')
#        else
#            print('UART: no data received')
        return data

    #def closeConnection(self):
    #    self.connection.close()
