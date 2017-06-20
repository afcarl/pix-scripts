# coding=utf-8
import requests
import json
import sys
from settings import AIRTABLE_BASE, AIRTABLE_API_KEY
from conf import ADAPTIVE_COURSE_IDS, SHORT_COURSE_ID


def make_request(request, extra_params={}):
    r = requests.get('https://api.airtable.com/v0/{}'.format(AIRTABLE_BASE) + request, headers={'Authorization': 'Bearer {}'.format(AIRTABLE_API_KEY)}, params={'maxRecords': 5, **extra_params})
    return r.json()

# print(json.dumps(make_request('/Épreuves'), indent=4))

def lookup_challenges(query):
    response = make_request({
        'filterByFormula': r"FIND(query, {Consigne})",
        'fields': ['Record ID', 'Consigne']
    })
    for entry in response['records']:
        print(entry['fields']['Record ID'], entry['fields']['Consigne'])

# print(json.dumps(req('/Tests'), indent=4))
"""records = req('/Épreuves').get('records')
if records:
    for entry in records:
        print(entry['fields']['Consigne'])
        print(entry['fields']['Propositions'])
        print 'GOOD:', entry['fields'].get(u'Bonnes réponses')
        print '-' * 42"""

# , params={'maxRecords': 20, 'filterByFormula': u"{Type d'épreuve} = 'QROC'"}

ADAPTIVE_COURSE_ID = ADAPTIVE_COURSE_IDS[SHORT_COURSE_ID]

with open('data/epreuves%s.json' % SHORT_COURSE_ID) as f:
    challenges = json.load(f)
    ids = set()
    for challenge in challenges:
        ids.add(challenge['id'])
    starter = open('data/starter%s.txt' % SHORT_COURSE_ID).read()
    ids.remove(starter)
    ids = [starter] + list(ids)
    # print(ids)

new_test = {'fields': {'Épreuves': ids[::-1]}}
# print(json.dumps(new_test))
r = requests.patch('https://api.airtable.com/v0/{}/Tests/%s'.format(AIRTABLE_BASE) % ADAPTIVE_COURSE_ID, headers={
        'Authorization': 'Bearer {}'.format(AIRTABLE_API_KEY), 'Content-type': 'application/json'}, data=json.dumps(new_test))
print(r.json())
