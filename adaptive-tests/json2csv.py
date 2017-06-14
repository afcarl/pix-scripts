import json

with open('data/scenarios.csv', 'w') as csvfile:
    with open('data/scenarios.json') as f:
        scenarios = json.load(f)['scenarios']
    for line in scenarios:
        csvfile.write(','.join(line) + '\n')
