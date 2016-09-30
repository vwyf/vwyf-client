# for caching questions and answers results
import sqlite3
# part of pymongo library, used for generating mongo objectId on client side
import bson
import logging
logging.basicConfig(filename='vwyf.log',level=logging.INFO)

import apiclient

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import utils

engine = create_engine('sqlite:///vwyf.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
# Session = sessionmaker()
# Session.configure(bind=engine)

class Question(Base):
  __tablename__ = 'questions'
  id = Column(String, primary_key=True)
  question = Column(String)
  option_a = Column(String)
  option_b = Column(String)
  created_at = Column(String)
  priority = Column(Integer)

  @staticmethod
  def _update_or_insert_question(question, session):
    record = session.query(Question).filter(Question.id==question.id).first()
    if (record):
      record.question = question.question
      record.option_a = question.option_a
      record.option_b = question.option_b
      record.priority = question.priority
    else:
      session.add(question);

  @staticmethod
  def update_or_insert_questions(questions):
    session = Session()
    for question in questions:
      _update_or_insert_question(question, session)
    session.commit()

class Answer(Base):
  __tablename__ = 'answers'
  id = Column(integer, primary_key=True)
  questionId = Column(String)
  answer = Column(String)
  created_at = Column(String)
  saved_to_server = Column(BOOLEAN)

class QuestionLog(Base):
  __tablename__ = 'question_logs'
  id = Column(integer, primary_key=True)
  questionId = Column(String)
  timestamp = StringCol()
  

# Question(questionId='my-q-id', question='how are you?', optionA='great', optionB='ok', priority=3)

Base.metadata.create_all(engine)


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
