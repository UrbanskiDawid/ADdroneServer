class FakeUartSender:
    connection = None

    def __init__(self):
        print('FakeUartSender constructed')

    def send(self, message):
        # print(str(message))
        pass

    def recv(self):
        return "adsasdasda"

    # TODO check if this method is needed
    def closeConnection(self):
        print('Connection closed')
