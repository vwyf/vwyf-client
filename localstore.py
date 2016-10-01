import logging

import utils
import apiclient
from models import Session, Question, Answer, QuestionLog

# log config
logging.basicConfig(filename='vwyf.log',level=logging.INFO)

def add_answer(questionId, answer):
  session = Session()
  answer = Answer(questionId = questionId, timestamp = util.ctime())
  session.add(answer)
  session.commit()

def log_question(questionId):
  session = Session()
  log = QuestionLog(questionId=questionId, timestamp=util.ctime())
  session.add(log)
  session.commit()

def _get_questions_map(questions):
  return dict(map(lambda q: (q.id, q), questions))

def sync_local_questions(remote_questions):
  session = Session()
  local_questions = session.query(Question).all()
  local_questions_map = _get_questions_map(local_questions)
  remote_questions_map = _get_questions_map(remote_questions)

  # insert or update questions
  for q in remote_questions:
    local_question = local_questions_map.get(q.id)
    if (local_question):
      local_question.question = q.question
      local_question.option_a = q.option_a
      local_question.option_b = q.option_b
      local_question.priority = q.priority
    else:
      session.add(q)

  # remove questions deleted from server
  for q in local_questions:
    if (not remote_questions_map.get(q.id)):
      session.delete(q)

  session.commit()


def get_next_question():
  #wip
  session = Session()
