import requests
import json
import logging

from models import Question

logging.basicConfig(filename='vwyf.log',level=logging.INFO)

# example_data = [
#   {'questionId': 'v3umMe2QdAa6HngJ6', 'answer': 'A', 'createdAt': 1474516715910 },
#   {'questionId': 'v3umMe2QdAa6HngJ6', 'answer': 'A', 'createdAt': 1474516716998 },
#   {'questionId': 'v3umMe2QdAa6HngJ6', 'answer': 'B', 'createdAt': 1474516761283 }
# ];

baseUrl = 'http://localhost:3000'
questionsUrl = baseUrl + '/questions'
answersUrl = baseUrl + '/answers'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def postAnswers(answers):
  requests.post(url, data=json.dumps(answers), headers=headers)

def getQuestions():
  r = requests.post(questionsUrl)
  parsed_json = json.loads(r.content)
  return map(lambda json: Question(json), parsed_json)
