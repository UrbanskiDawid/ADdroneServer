import sqlite3

class Logger:
  conn = None;

  def __init__(self):
    self.conn = sqlite3.connect('test.db')
    self.conn.execute('''CREATE TABLE RECEIVED
       (ID INT PRIMARY KEY     NOT NULL,
       TIME           INT      NOT NULL,
       SRC_ADDR       TEXT     NOT NULL);''')

  def logReceivedMessage(self, srcAddr):
    self.conn.execute('''("INSERT INTO RECEIVED (ID,TIME,SRC_ADD) \
                           VALUES (0, 0, '0.0.0.0')");''')
