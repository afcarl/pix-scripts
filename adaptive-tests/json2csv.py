import json
from conf import SHORT_COURSE_ID


with open('data/scenarios%s.csv' % SHORT_COURSE_ID, 'w') as csvfile:
    with open('data/scenarios%s.json' % SHORT_COURSE_ID) as f:
        scenarios = json.load(f)['scenarios']
    for line in scenarios:
        csvfile.write(','.join(line) + '\n')
