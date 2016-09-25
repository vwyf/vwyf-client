import logging

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

class Question:
  def __init__(self, json):
    self._id = json['_id']
    self.text = json['text']
    self.optionA = json['optionA']
    self.optionB = json['optionB']
    self.priority = json['priority']
    self.createdAt = json['createdAt']
