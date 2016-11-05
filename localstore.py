import random
import logging
from sqlalchemy import func

import utils
import apiclient
from models import Session, Question, Answer, QuestionLog

# log config
logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# maintain a local cache of all votes collected
local_vote_counts_map = dict(map(
  lambda q: (q.id, {'A': q.count_a, 'B': q.count_b}),
  Session().query(Question).all()
))

def _get_current_ratio(question_id, answer_to_add=None):
  if (not local_vote_counts_map.get(question_id)):
    logging.info("Inilizing new local counts for question: " + question_id)
    local_vote_counts_map[question_id] = {'A': 0, 'B': 0}

  local_counts = local_vote_counts_map[question_id]

  if (answer_to_add):
    local_counts[answer_to_add] += 1

  # smoothen the ratio when starting a new question
  if (local_counts['A'] < 5 or local_counts['B'] < 5):
    return (local_counts['A'] + 5) / float(local_counts['A'] + local_counts['B'] + 10)

  return local_counts['A'] / float(local_counts['A'] + local_counts['B'])

def add_answer(question_id, answer):
  session = Session()
  answerObj = Answer(
      question_id = question_id,
      answer=answer,
      created_at = utils.ctime())
  session.add(answerObj)
  session.commit()
  return _get_current_ratio(question_id, answer)

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


# Question Weight:
# 0 answer collected: 20x
# urgent: 0, weight 5x
# hight: 1, weight 3x
# medium: 2, weight 2x
# low: 3, weight 1x
# turned off: 4, weight 0x
def _get_question_weight(q):
  if (q.count_a == 0 and q.count_b == 0):
    return 20
  else:
    return {
      0: 5,
      1: 3,
      2: 2,
      3: 1,
      4: 0
    }[q.priority]

def _weighted_choice(questions):
  total = sum(_get_question_weight(q) for q in questions)
  r = random.uniform(0, total)
  upto = 0
  for q in questions:
    w = _get_question_weight(q)
    if upto + w >= r:
      return q
    upto += w
  raise Exception('should not go here')

# Randomly choose next question to display, based on weight
def get_next_question():
  session = Session()
  all_questions = session.query(Question).all()

  if (len(all_questions) <= 0):
    logging.error('Question list is empty.')
    return

  return _weighted_choice(all_questions)



