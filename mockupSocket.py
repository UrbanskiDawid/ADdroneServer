import time

class mockupSocket:
    address = None
    dataIndex = 0
    data = []

    def __init__(self, repeat):
        print("mockupSocket constructed")
        fname = "tools/clientSimulator/sequences/start"
        with open(fname) as f:
            content = f.readlines()
            f.close()
        for line in content:
            datastring = self.HexDelimitedStringToDataString(line.rstrip())
            self.data.append(datastring)
        print("ip data loaded from file :", fname)
        self.__repeat = repeat
        print("repeat sequence = " + str(self.__repeat))

    def HexDelimitedStringToDataString(self, line):
        hexstr_list = line.split(",")
        str_list = [chr(int(item)) for item in hexstr_list]
        data = ''.join(str_list)
        return data

    def bind(self, address):
        self.address = address

    def accept(self):
        return self, self.address

    def listen(self, backlog):
        pass

    def send(self, message):
        pass

    def recv(self, bufferSize):
        sleepTime = 0.05
        ret_data = self.data[self.dataIndex]
        if self.dataIndex >= len(self.data) - 1:
            if self.__repeat:
                self.dataIndex = 0
            else:
                sleepTime = 1.0
                ret_data = None
        else:
            self.dataIndex += 1

#        if ret_data:
#            print("Data index: " + str(self.dataIndex))

        time.sleep(sleepTime)
        return ret_data

    def close(self):
        pass
