import logging
from sqlalchemy import func

import utils
import apiclient
from models import Session, Question, Answer, QuestionLog

# log config
logging.basicConfig(filename='vwyf.log',level=logging.INFO)

def add_answer(question_id, answer):
  session = Session()
  answer = Answer(
      question_id = question_id,
      answer=answer,
      created_at = utils.ctime())
  session.add(answer)
  session.commit()

# log means question currently being displayed
# If application is healthy, this should be called every one minute
def log_question(question_id):
  session = Session()
  log = QuestionLog(
      question_id=question_id,
      timestamp=utils.ctime())
  session.add(log)
  session.commit()

def _get_questions_id_map(questions):
  return dict(map(lambda q: (q.id, q), questions))

def update_local_questions(remote_questions):
  session = Session()
  local_questions = session.query(Question).all()
  local_questions_map = _get_questions_id_map(local_questions)
  remote_questions_map = _get_questions_id_map(remote_questions)

  # insert or update questions
  for q in remote_questions:
    local_question = local_questions_map.get(q.id)
    if (local_question):
      local_question.question = q.question
      local_question.option_a = q.option_a
      local_question.option_b = q.option_b
      local_question.priority = q.priority
      local_question.created_at = q.created_at
      local_question.count_a = q.count_a
      local_question.count_b = q.count_b
    else:
      session.add(q)

  # remove questions deleted from server
  for q in local_questions:
    if (not remote_questions_map.get(q.id)):
      session.delete(q)

  session.commit()

def save_answers_to_server(post):
  session = Session()

  # pull 50 unsaved answers from local db
  recent_unsaved_answers = session.query(Answer).limit(50).all()

  # post answers to server and set saved flag when post succeeded
  if (len(recent_unsaved_answers) > 0 and post(recent_unsaved_answers)):
    for ans in recent_unsaved_answers:
      session.delete(ans)

    session.commit()
    return True

  return False

# Returning a dictionary containing (question_id -> # of logs)
# e.g. {u'wM7MC2EJHAAtHk9ms': 105, u'yxmb4H2KJsGxvpKKD': 328}
def _get_question_logs_map(session = Session()):
  question_id_count_pairs = session.query(
      QuestionLog.question_id, func.count(QuestionLog.id)).\
      group_by(QuestionLog.question_id).\
      all()
  return dict(question_id_count_pairs)


# priority: urgent: 0, hight: 1, medium: 2, low: 3
def get_next_question():
  session = Session()
  all_questions = session.query(Question).all()

  if (len(all_questions) <= 0):
    logging.error('Question list is empty.')
    return

  question_logs_map = _get_question_logs_map(session)

  def getKey(q):
    num_of_logs = question_logs_map.get(q.id, 0)
    return (num_of_logs + 1) * (q.priority + 3)
  
  return sorted(all_questions, key=getKey)[0]

