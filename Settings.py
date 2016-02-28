import ConfigParser

class Settings:

  #DEFAULT VALUES
  PORT=5555
  BINDRETRYNUM=3

  UARTDEVICE=""
  UARTBAUNDRATE=9600

  def __init__(self):
    config = ConfigParser.RawConfigParser()
    config.read('ADdrone.cfg')

    self.PORT = config.getint('SERVER', 'port')
    self.BINDRETRYNUM = config.getint('SERVER', 'bindRetryNum')

    if config.has_section('UART'):
      self.UARTDEVICE = config.get('UART','device')
      self.UARTBAUNDRATE = config.getint('UART','baundrate')

