import logging

import apiclient
import localstore

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# interface for flipdot daemon
class DataManager:
  def __init__(self):
    logging.info('initializing DataManager')
    # start syncing questions/answers with server

  def getNextQuestion():
    # select logs
    return 1

  def vote(self, questionId, isVoteA):
    answer = 'A' if isVoteA else 'B'
    localstore.addAnswer(questionId, answer)

  def log(questionId):
    logQuestion(questionId)
