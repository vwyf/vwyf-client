import logging

import utils
import apiclient
from models import session, Question, Answer, QuestionLog

# log config
logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# Question(questionId='my-q-id', question='how are you?', optionA='great', optionB='ok', priority=3)

def addAnswer(questionId, answer):
  session.Session()
  answer = Answer(questionId = questionId, timestamp = util.ctime())
  session.add(answer)
  session.commit()

def logQuestion(questionId):
  session.Session()
  log = QuestionLog(questionId=questionId, timestamp=util.ctime())
  session.add(log)
  session.commit()

def _update_or_insert_question(question, session):
  record = session.query(Question).filter(Question.id==question.id).first()
  if (record):
    record.question = question.question
    record.option_a = question.option_a
    record.option_b = question.option_b
    record.priority = question.priority
  else:
    session.add(question);

def update_or_insert_questions(questions):
  session = Session()
  for question in questions:
    _update_or_insert_question(question, session)
  session.commit()

# def addAnswer(conn, questionId, answer):
#   now = utils.ctime()
#   c = conn.cursor()
#   c.execute(
#       '''INSERT INTO answers (questionId, answer, createdAt) VALUES (?, ?, ?)''',
#       (questionId, answer, now))
#   conn.commit()
#   logging.info("{now!s}: added new answer: {questionId!s} {answer!s}".format(**locals()))

# def syncAnswers(conn):
#   c = conn.cursor()
#   c.execute('''
#       SELECT * FROM answers
#       WHERE savedToServer == 0
#       ORDER BY createdAt
#       LIMIT 50
#       ''')
#   answers = c.fetchall()
#   apiclient.postAnswers(map(_toAnswerDict, answers))

# def getAllQuestions(conn):
#   c = conn.cursor()
#   c.execute('''
#       SELECT * FROM questions 
#       ''')
#   questions = c.fetchall()
#   return map(Question.fromSql, question)

# def _toAnswerDict(ansArr):
#   return { 'questionId': ansArr[1], 'answer': ansArr[2], 'createdAt': ansArr[3] }

# if __name__ == "__main__":
#   conn = sqlite3.connect('vwyf.db')
#   init(conn)
#   conn.close()
