import configparser

class Settings:

    #DEFAULT VALUES
    #SERVER section
    PORT = 5555
    BINDRETRYNUM = 3
    SIMULATOR = False

    #UART section
    UARTDEVICE = ""
    UARTBAUDRATE = 9600
    UARTSIMULATOR = False

    def __init__(self):
        config = configparser.RawConfigParser()
        config.read('ADdrone.cfg')

        if config.has_section('SERVER'):
            self.PORT = config.getint('SERVER', 'port')
            self.BINDRETRYNUM = config.getint('SERVER', 'bindRetryNum')
            self.SIMULATOR = config.getboolean('SERVER', 'simulator', fallback=False)

        if config.has_section('UART'):
            self.UARTDEVICE = config.get('UART', 'device')
            self.UARTBAUDRATE = config.getint('UART', 'baudrate')
            self.UARTSIMULATOR = config.getboolean('UART', 'simulator', fallback=False)
