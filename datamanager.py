import logging
import apiclient
from localstore import *

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

class DataManager:
  def __init__(self):
    logging.info('initializing DataManager')
    # start syncing questions/answers with server

  def __del__(self):
    logging.info('deleting DataManager')
    # stop syncing questions/answers with server

  def getNextQuestion():
    return 1

  def vote(self, questionId, isVoteA):
    answer = 'A' if isVoteA else 'B'
    localstore.addAnswer(self.conn, questionId, answer)

  def log(questionId):
    session = Session()
    log = QuestionLog(questionId=questionId, timestamp=utils.ctime())
    session.add(log)
    session.commit()
