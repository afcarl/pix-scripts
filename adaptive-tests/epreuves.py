import csv
from collections import Counter
import json
import sys
from conf import SHORT_COURSE_ID


# Airtable to JSON
with open('data/Epreuves-JJV%s.csv' % SHORT_COURSE_ID) as f:
    csvreader = csv.reader(f)
    fields = next(f).split(',')
    data = []
    addons = []
    c = Counter()
    for line in csvreader:
        data.append(dict(zip(fields, line)))
        current = data[-1]
        """for k in current:
            print(k, current[k])
        break"""
        if True: #current['compétence'].startswith('1.3.') and not current['acquis'].endswith('6'):
            c[current['acquis']] += 1 # current['_Niveau'] is not useful anymore
            addons.append({
                'id': current['Record ID'],
                'statement': current['\ufeffConsigne'],
                'tags': current['acquis']
            })
    for k in sorted(c.keys()):
        print(k, c[k])

# Save it
with open('data/epreuves%s.json' % SHORT_COURSE_ID, 'w') as f:
    json.dump(addons, f, indent=True)

# Infer the graph of prerequisites
nodes = sorted(c.keys())
n = len(nodes)
inv = {nodes[i]: i for i in range(n)}
edges = []
for i in range(n - 1):
    if nodes[i][:-1] == nodes[i + 1][:-1]:  # Hack
        edges.append((i, i + 1))
with open('data/prerequis%s.json' % SHORT_COURSE_ID, 'w') as f:
    f.write(json.dumps({'nodes': nodes, 'edges': edges, 'inv': inv}));
