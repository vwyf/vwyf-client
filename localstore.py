# for caching questions and answers results
import sqlite3
# part of pymongo library, used for generating mongo objectId on client side
import bson
import time
import logging
from models import Question

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

def _ctime():
  return str(int(time.time() * 1000))

def init():
  conn = sqlite3.connect('vwyf.db')
  createTable(conn)
  conn.close()

def createTable(conn):
  logging.info("Initializing SQLite Table..")
  c = conn.cursor()
  c.execute('''
      CREATE TABLE IF NOT EXISTS questions (
        questionId TEXT UNIQUE,
        question TEXT,
        optionA TEXT,
        optionB TEXT,
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

def addAnswer(conn, questionId, answer):
  now = _ctime()
  c = conn.cursor()
  c.execute(
      '''INSERT INTO answers (questionId, answer, createdAt) VALUES (?, ?, ?)''',
      (questionId, answer, now))
  conn.commit()
  logging.info("{now!s}: added new answer: {questionId!s} {answer!s}".format(**locals()))

def syncAnswers():
  c = conn.cursor()
  c.execute('''
      SELECT * FROM answers
      WHERE savedToServer == 0
      ORDER BY createdAt
      LIMIT 50
      ''')
  answers = c.fetchall()

if __name__ == "__main__":
  init()
