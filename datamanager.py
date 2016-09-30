import logging
import apiclient
import localstore

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

class DataManager:
  def __init__(self):
    logging.info('initializing DataManager')
    self.conn = conn = sqlite3.connect('vwyf.db')

  def __del__(self):
    logging.info('deleting DataManager')
    self.conn.close()

  def getNextQuestion():
    return 1

  def vote(self, questionId, isVoteA):
    answer = 'A' if isVoteA else 'B'
    localstore.addAnswer(self.conn, questionId, answer)
