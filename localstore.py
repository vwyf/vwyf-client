# for caching questions and answers results
import sqlite3
# part of pymongo library, used for generating mongo objectId on client side
import bson
import time
import logging
import apiclient
from models import Question

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

def _ctime():
  return str(int(time.time() * 1000))

def init(conn):
  _createTable(conn)

def _createTable(conn):
  logging.info("Initializing SQLite Table..")
  c = conn.cursor()
  c.execute('''
      CREATE TABLE IF NOT EXISTS questions (
        questionId TEXT UNIQUE,
        question TEXT,
        optionA TEXT,
        optionB TEXT,
        priority INTEGER,
        timesUsed INTEGER DEFAULT 0
      )''')
  c.execute('''
      CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        questionId TEXT,
        answer TEXT, 
        createdAt TEXT,
        savedToServer INTEGER DEFAULT 0
      )''')
  conn.commit()

def addOrUpdateQuestion(conn, q):
  c = conn.cursor()
  c.execute('''
    INSERT INTO questions (questionId, question, optionA, optionB, priority createdAt)
    VALUES (?, ?, ?, ?, ?, ?)''', (q._id, q.text, q.optionA, q.optionB, q.priority, q.createdAt))
  conn.commit()

def addAnswer(conn, questionId, answer):
  now = _ctime()
  c = conn.cursor()
  c.execute(
      '''INSERT INTO answers (questionId, answer, createdAt) VALUES (?, ?, ?)''',
      (questionId, answer, now))
  conn.commit()
  logging.info("{now!s}: added new answer: {questionId!s} {answer!s}".format(**locals()))

def syncAnswers(conn):
  c = conn.cursor()
  c.execute('''
      SELECT * FROM answers
      WHERE savedToServer == 0
      ORDER BY createdAt
      LIMIT 50
      ''')
  answers = c.fetchall()
  apiclient.postAnswers(map(_toAnswerDict, answers))

def getAllQuestions(conn):
  c = conn.cursor()
  c.execute('''
      SELECT * FROM questions 
      ''')
  questions = c.fetchall()
  return map(Question.fromSql, question)

def _toAnswerDict(ansArr):
  return { 'questionId': ansArr[1], 'answer': ansArr[2], 'createdAt': ansArr[3] }

if __name__ == "__main__":
  conn = sqlite3.connect('vwyf.db')
  init(conn)
  conn.close()
