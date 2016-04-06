import ConfigParser

class Settings:

    #DEFAULT VALUES
    #SERVER section
    PORT = 5555
    BINDRETRYNUM = 3
    TCPSIMULATOR = False

    #UART section
    UARTDEVICE = ""
    UARTBAUDRATE = 9600
    UARTSIMULATOR = False

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('ADdrone.cfg')

        if config.has_section('SERVER'):
            self.PORT = config.getint('SERVER', 'port')
            self.BINDRETRYNUM = config.getint('SERVER', 'bindRetryNum')
            if config.has_option('SERVER', 'simulator'):
                self.TCPSIMULATOR = config.getboolean('SERVER', 'simulator')

        if config.has_section('UART'):
            self.UARTDEVICE = config.get('UART', 'device')
            self.UARTBAUDRATE = config.getint('UART', 'baudrate')
            if config.has_option('UART', 'simulator'):
                self.UARTSIMULATOR = config.getboolean('UART', 'simulator')
