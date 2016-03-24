import unittest
from Message import *

class MessageTest(unittest.TestCase):
    def test_isValidCommand_emptyMessage_False(self):
        sut = Message('')
        result = sut.isValid()
        self.assertEqual(result, False)

    def test_isValidCommand_randomInvalidMessage_False(self):
        sut = Message('Some random invalid message')
        result = sut.isValid()
        self.assertEqual(result, False)

    def test_isValidCommand_basicValidMessage_True(self):
        ''' Now it fails! '''
        sut = Message('$$$$ffffffffffffffffkkm000000000000000')
        result = sut.isValid()
        self.assertEqual(result, True)

if __name__ == '__main__':
        unittest.main()