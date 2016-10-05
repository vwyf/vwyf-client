import logging

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# log config
logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# sql alchemy config
engine = create_engine('sqlite:///vwyf.db', echo=False, connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)

# q = Question(id='my-q-id', question='how are you?', option_a='great', option_b='ok', priority=3, created_at='12312312312321')

class Question(Base):
  __tablename__ = 'questions'
  id = Column(String, primary_key=True)
  question = Column(String)
  option_a = Column(String)
  option_b = Column(String)
  created_at = Column(String)
  priority = Column(Integer)
  count_a = Column(Integer)
  count_b = Column(Integer)

  @classmethod
  def from_json(cls, json):
    return cls(
        id=json['_id'],
        question=json['text'],
        option_a=json['optionA'],
        option_b=json['optionB'],
        priority=json['priority'],
        created_at=json['createdAt'],
        count_a=json['count']['A'],
        count_b=json['count']['B'])

class Answer(Base):
  __tablename__ = 'answers'

  id = Column(Integer, primary_key=True)
  question_id = Column(String, index=True)
  answer = Column(String)
  created_at = Column(String)

  def to_json(self):
    return {
        'questionId': self.question_id,
        'answer': self.answer,
        'createdAt': self.created_at
        }

class QuestionLog(Base):
  __tablename__ = 'question_logs'

  id = Column(Integer, primary_key=True)
  question_id = Column(String, index=True)
  timestamp = Column(String)

Base.metadata.create_all(engine)
