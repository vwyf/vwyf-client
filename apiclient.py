import requests
import json
import logging

from models import Session, Question, Answer 
import localstore

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# example_data = [
#   {'questionId': 'v3umMe2QdAa6HngJ6', 'answer': 'A', 'createdAt': 1474516715910 },
#   {'questionId': 'v3umMe2QdAa6HngJ6', 'answer': 'A', 'createdAt': 1474516716998 },
#   {'questionId': 'v3umMe2QdAa6HngJ6', 'answer': 'B', 'createdAt': 1474516761283 }
# ];

baseUrl = 'http://localhost:3000'
questions_url = base_url + '/questions'
answers_url = base_url + '/answers'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def post_answers(answers):
  requests.post(answers_url, data=json.dumps(answers), headers=headers)

# JSON response format:
# [{u'_id': u'yQmghShgFbbFE4Zgg',
#   u'createdAt': u'2016-10-01T19:59:15.245Z',
#   u'optionA': u'Yes',
#   u'optionB': u'No',
#   u'priority': 3,
#   u'text': u'Are you happy?'}]

def get_questions():
  r = requests.post(questions_url)
  if (r.status_code != 200):
    logging('REQUEST FAILD in synclocalquestions failed')
    return (False, []) # request failed

  parsed_json = json.loads(r.content)
  questions = map(lambda json: Question.from_json(json), parsed_json)
  return (True, questions)
