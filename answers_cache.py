# for caching questions and answers results
import sqlite3
# part of pymongo library, used for generating mongo objectId on client side
import bson
import datetime

def ctime():
  datetime.datetime.now().ctime()

def init():
  conn = sqlite3.connect('answers.db')
  createTable(conn)
  conn.close()

def createTable(conn):
  print "Initializing Table"
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS answers (
      id INTEGER AUTOINCREMENT,
      questionsId TEXT,
      answer INTEGER,
      createdAt TIMESTAMP,
      savedToServer INTEGER DEFAULT 0
      )''')
  conn.commit()

def addNewAnswer(questionId, answer):
  now = ctime()
  c = conn.cursor()
  c.execute('''INSERT INTO answers (questionId, answer, createdAt) VALUES (?, ?, ?)''',
      (questionId, answer, now))
  conn.commit()
  print "{now!s}: added new answer: {questionId!s} {answer!s}".format(**locals())

def syncAnswers(batch = 10):
  #todo
  return

if __name__ == "__main__":
  init()
