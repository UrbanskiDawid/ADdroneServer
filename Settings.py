import ConfigParser

class Settings:

  #DEFAULT VALUES
  PORT=5555
  BINDRETRYNUM=3

  def __init__(self):
    config = ConfigParser.RawConfigParser()
    config.read('ADdrone.cfg')
    self.PORT = config.getint('SERVER', 'port')
    self.BINDRETRYNUM = config.getint('SERVER', 'bindRetryNum')
