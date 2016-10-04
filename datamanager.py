import logging

import apiclient
import localstore

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# interface for flipdot daemon
def getNextQuestion():
  return localstore.get_next_question()

def vote(self, question_id, isVoteA):
  answer = 'A' if isVoteA else 'B'
  localstore.addAnswer(question_id, answer)

def log(question_id):
  localstore.log_question(question_id)

# blocking network call
def sync_questions_with_server():
  (fetched, questions) = apiclient.get_questions()

  if (fetched):
    localstore.update_local_questions(questions);

# blocking network call
def save_answers_to_server():
  localstore.save_answers_to_server(apiclient.post_answers)
