import logging

import apiclient
import localstore

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# interface for flipdot daemon
def get_next_question():
  return localstore.get_next_question()

def vote(question_id, isVoteA):
  answer = 'A' if isVoteA else 'B'
  localstore.add_answer(question_id, answer)

def log(question_id):
  localstore.log_question(question_id)

# blocking network call
def sync_questions_with_server():
  (fetched, questions) = apiclient.get_questions()

  if (fetched):
    localstore.update_local_questions(questions);

  return fetched

# blocking network call
def save_answers_to_server():
  return localstore.save_answers_to_server(apiclient.post_answers)
