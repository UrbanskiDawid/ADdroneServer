

class FakeUartSender:
    connection = None

    def __init__(self):
        print('UartSender constructed')

    def send(self, message):
        print(str(message))
        '''print(message + ' sent over UART')'''

    def closeConnection(self):
        print('Connection closed')
