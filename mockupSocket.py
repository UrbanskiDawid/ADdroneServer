import time

class mockupSocket:
    address = None
    dataIndex = 0
    data = []

    def __init__(self):
        print("mockupSocket constructed")
        self.data.append("$$$$12213213243534534FFFFFFFFFFFFFFFFF")
        self.data.append("$$$$12213213243534534EEEEEEEE000000000")

    def bind(self, address):
        self.address = address

    def accept(self):
        return self, self.address

    def listen(self, backlog):
        pass

    def send(self, message):
        pass

    def recv(self, bufferSize):
        time.sleep(0.1)
        ret_data = self.data[self.dataIndex]
        if self.dataIndex >= len(self.data) - 1:
            self.dataIndex = 0
        else:
            self.dataIndex += 1
        return ret_data

    def close(self):
        pass
