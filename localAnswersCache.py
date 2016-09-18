# for caching questions and answers results
import sqlite3
# part of pymongo library, used for generating mongo objectId on client side
import bson

def init():
  conn = sqlite3.connect('answers.db')
  createTable(conn)
  conn.close()

def createTable(conn):
  c = conn.cursor()
  c.execute('''create table if not exists answers (
      answerId TEXT,
      questionsId TEXT,
      answer INTEGER,
      createdAt TIMESTAMP,
      savedToServer INTEGER DEFAULT 0
      )''')
  conn.commit()
  print "done"

if __name__ == "__main__":
  init()
