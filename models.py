import logging

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

class Question:
  def __init__(self, _id, text, optionA, optionB, priority, createdAt):
    self._id = _id
    self.text = text
    self.optionA = optionA
    self.optionB = optionB
    self.priority = priority
    self.createdAt = createdAt

  @classmethod
  def fromJson(cls, json):
    return cls(
        json['_id'],
        json['text'],
        json['optionA'],
        json['optionB'],
        json['priority'],
        json['createdAt'])

  @classmethod
  def fromSql(cls, questionArr):
    return cls(
        questionArr[0],
        questionArr[1],
        questionArr[2],
        questionArr[3],
        questionArr[4],
        questionArr[5],
        questionArr[6])
