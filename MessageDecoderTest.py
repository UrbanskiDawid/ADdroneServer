import unittest
from MessageDecoder import *

class MessageDecoderTest(unittest.TestCase):
  def test_tryToReadMessage_emptyMessage_false(self):
    sut = MessageDecoder()
    result = sut.tryToReadMessage('')
    self.assertEqual(result, False)

  def test_tryToReadMessage_randomInvalidMessage_false(self):
    sut = MessageDecoder()
    result = sut.tryToReadMessage('Some random invalid message')
    self.assertEqual(result, False)

if __name__ == '__main__':
    unittest.main()