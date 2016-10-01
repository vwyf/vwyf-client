import logging

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# log config
logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# sql alchemy config
engine = create_engine('sqlite:///vwyf.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Question(Base):
  __tablename__ = 'questions'

  id = Column(String, primary_key=True)
  question = Column(String)
  option_a = Column(String)
  option_b = Column(String)
  created_at = Column(String)
  priority = Column(Integer)

class Answer(Base):
  __tablename__ = 'answers'

  id = Column(Integer, primary_key=True)
  questionId = Column(String, index=True)
  answer = Column(String)
  created_at = Column(String)
  saved_to_server = Column(Boolean)

class QuestionLog(Base):
  __tablename__ = 'question_logs'

  id = Column(Integer, primary_key=True)
  questionId = Column(String, index=True)
  timestamp = Column(String)

Base.metadata.create_all(engine)

# class Question:
#   def __init__(self, _id, text, optionA, optionB, priority, createdAt):
#     self._id = _id
#     self.text = text
#     self.optionA = optionA
#     self.optionB = optionB
#     self.priority = priority
#     self.createdAt = createdAt

#   @classmethod
#   def fromJson(cls, json):
#     return cls(
#         json['_id'],
#         json['text'],
#         json['optionA'],
#         json['optionB'],
#         json['priority'],
#         json['createdAt'])

#   @classmethod
#   def fromSql(cls, questionArr):
#     return cls(
#         questionArr[0],
#         questionArr[1],
#         questionArr[2],
#         questionArr[3],
#         questionArr[4],
#         questionArr[5],
#         questionArr[6])
