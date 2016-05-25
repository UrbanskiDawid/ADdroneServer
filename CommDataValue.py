from struct import *
from CommData import *

class CommDataValue:

    # preamble and CRC is present in every communication data
    preamble = "$$$$"
    CRC = None
    
    def __init__(self, commData = None):
        pass

    def getCommData(self):
        pass

    def toString(self):
        pass

    def __str__(self): 
        return toString()
