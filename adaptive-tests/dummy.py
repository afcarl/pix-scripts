import json
from collections import Counter, namedtuple
from itertools import product
from logreg import proba, compute_level_est
from graph import generate_display
import sys


MAX_DEPTH = int(sys.argv[1])
ADAPTIVE_COURSE_ID = sys.argv[2]


with open('data/prerequis.json') as f:
    data = json.load(f)
    nodes = data['nodes']
    edges = data['edges']
    inv = data['inv']
    n = len(nodes)
    print(n, 'nodes')

id_of = {}
statement_of = {}
with open('data/epreuves.json') as f:
    problems = json.load(f)
    for problem in problems:
        id_of[problem['tags']] = problem['id']
        statement_of[problem['tags']] = problem['statement']
        # print(id_of[problem['tags']])

cat = [None] * ((1 << MAX_DEPTH) - 1)
next_question = {}
yes_of = {'': []}
no_of = {'': []}
level_est_of = {'': 3}
history_of = {'': []}

def propagate_acquix(i, outcome): # already, 
    # print('already', already)
    step = -1 if outcome == 1 else 1
    new = [i]
    c = i
    while 0 <= c + step < n and nodes[c + step][:-1] == nodes[c][:-1]:# and c + step not in already:
        new.append(c + step)
        c += step
    return new

parents = [[] for _ in range(n)]
children = [[] for _ in range(n)]
for i in range(n):
    parents[i] = propagate_acquix(i, 1)
    children[i] = propagate_acquix(i, 0)

def level_of(node):
    return int(node[-1])  # To be changed

def get_best(path, yes, no, level_est):
    # contestants = Counter()
    best_i = None
    best_score = 0
    already = set(yes + no)
    not_already = set(range(n)) - already
    if_sets = None
    if not not_already:
        return None
    for i in not_already: #enumerate(nodes):
        node = nodes[i]
        # if i in already:
        #     continue
        # print(i, node)
        proba_yes = proba(level_est, level_of(node))
        if proba_yes < 1e-1:  # Do not ask too hard questions
            continue
        #if_yes = propagate_acquix(already, i, 1)
        #if_no = propagate_acquix(already, i, 0)
        if_yes = set(parents[i]) - already
        if_no = set(children[i]) - already
        # contestants[i] = -(abs(len(if_yes) - len(if_no)) - len(if_yes) - len(if_no))  # Old formula
        score = proba_yes * len(if_yes) + (1 - proba_yes) * len(if_no)
        if score > best_score:
            best_score = score
            best_i = i
            if_sets = (if_yes, if_no)
    # best_i = contestants.most_common(1)[0][0]
    """for k, v in contestants.most_common(5):
        print(nodes[k], v)"""
    # print(best_i)
    if best_i is None:
        return None
    return best_i, (list(if_sets[0]), list(if_sets[1]))

def get_all_pos_of(path):
    pos = [0]
    c = 0
    for letter in path:
        if letter == '0':
            c = c * 2 + 1
        if letter == '1':
            c = c * 2 + 2
        pos.append(c)
    return pos

def get_level_est(path): # , cat
    """pos = get_all_pos_of(path)
    history = []
    for i, letter in enumerate(path):
        history.append((level_of(nodes[cat[pos[i]]]), path[i] == '1'))"""
    return compute_level_est(history_of[path])


Stage = namedtuple('Stage', 'path acquired not_acquired level_est history')


command = {'': '', '1': 'ok', '0': 'ko'}
if __name__ == '__main__':
    display_cat = [None] * ((1 << MAX_DEPTH) - 1)
    nb_null = 0
    paths = ['']
    """for depth in range(MAX_DEPTH):
        for path in product('01', repeat=depth):"""
    while paths:
        path = paths.pop()
        if len(path) >= MAX_DEPTH:
            continue
        # path = ''.join(path)
        best = get_best(path, yes_of[path], no_of[path], level_est_of[path])
        if not best:
            nb_null += 1
            continue
        best_i, (if_yes, if_no) = best
        paths.extend([path + '0', path + '1'])
        c = get_all_pos_of(path)[-1]
        # cat[c] = best_i
        next_question[command[path]] = best_i
        # print(path, best_i)
        display_cat[c] = '%.1f %s ?' % (level_est_of[path], nodes[best_i])
        if c == 0:
            print('Starts with:', id_of[nodes[best_i]])
            print(statement_of[nodes[best_i]])
        # print(c, best_i)
        yes_of[path + '0'] = yes_of[path]
        no_of[path + '0'] = no_of[path] + if_no
        yes_of[path + '1'] = yes_of[path] + if_yes
        no_of[path + '1'] = no_of[path]
        if path:
            command[path + '0'] = command[path] + '-ko'
            command[path + '1'] = command[path] + '-ok'
        history_of[path + '0'] = history_of[path] + [(level_of(nodes[best_i]), False)]
        history_of[path + '1'] = history_of[path] + [(level_of(nodes[best_i]), True)]
        level_est_of[path + '0'] = get_level_est(path + '0')#, cat)
        # print(get_level_est(path + '0', cat))
        level_est_of[path + '1'] = get_level_est(path + '1')#, cat)
        # print(path)
    print(len(yes_of), (1 << MAX_DEPTH + 1) - 1)
    print(nb_null, 'avoided null-nodes')
    # print(cat)
    '''if MAX_DEPTH <= 5:
        generate_display(display_cat)'''
    # print(no)

records = []
for path in next_question:
    if path:
        # print(path, nodes[next_question[path]])
        records.append([ADAPTIVE_COURSE_ID, path, id_of[nodes[next_question[path]]]])

with open('data/scenarios.json', 'w') as f:
    f.write(json.dumps({'scenarios': records}))
