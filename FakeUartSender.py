class FakeUartSender:
    connection = None

    def __init__(self):
        print('FakeUartSender constructed')

    def send(self, message):
        print(str(message))

    def recv(self):
        return "adsasdasda"

    # def closeConnection(self):
    #     print('Connection closed')
