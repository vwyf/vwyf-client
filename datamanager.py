import logging

import apiclient
import localstore

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# interface for flipdot daemon
def get_next_question():
  q = localstore.get_next_question()
  return q.id, q.question, q.option_a, q.option_b

def log_vote(question_id, isVoteA):
  answer = 'A' if isVoteA else 'B'
  localstore.add_answer(question_id, answer)

def log_question(question_id):
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
