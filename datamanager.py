import logging
import threading
import time

import apiclient
import localstore

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# interface for flipdot daemon
def get_next_question():
  q = localstore.get_next_question()
  return q.id, q.question, q.option_a, q.option_b

# return current ratio (#ofA) / (#ofAllVotes)
def log_vote(question_id, isVoteA):
  answer = 'A' if isVoteA else 'B'
  return localstore.add_answer(question_id, answer)

def log_question(question_id):
  localstore.log_question(question_id)

# blocking network call
def _sync_questions_with_server():
  logging.info('fetching questions')
  fetched, questions = apiclient.get_questions()

  logging.info('fetched questions' + str(fetched))
  if (fetched):
    logging.info('updating questions')
    localstore.update_local_questions(questions);

  return fetched

# blocking network call
def _save_answers_to_server():
  return localstore.save_answers_to_server(apiclient.post_answers)

def _data_daemon_worker():
  num_of_loops = 0
  while True:
    num_of_loops += 1
    try:
      logging.info("running data daemon loop: " + str(num_of_loops))
      _sync_questions_with_server()
      _save_answers_to_server()
      time.sleep(180)
    except:
      logging.error("data daemon loop failed at: " + str(num_of_loops))
      time.sleep(300)

# Note that we set 'check_same_thread' to false for sqlalchemy To avoid potential
# concurrency issue with SQLite:
# 1) only the main thread can write to answers and question_logs table
# 2) only the data daemon thread can write to questions table
def start_data_daemon():
  data_daemon = threading.Thread(target=_data_daemon_worker)
  data_daemon.daemon = True
  data_daemon.start()
