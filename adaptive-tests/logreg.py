# from sklearn.linear_model import LogisticRegression
# import numpy as np
# from scipy.optimize import brentq
from math import exp, log
import random

# Learner
# level = 3

# Questions
# diff = np.arange(1, 7, 1)
# nb_questions = len(diff)

def proba(theta, d):
    return 1 / (1 + exp(-(theta - d)))

# Noisy response pattern
# print([proba(level, diff[i]) for i in range(nb_questions)])
# pattern = [random.random() < proba(level, diff[i]) for i in range(nb_questions)]
# pattern = [round(proba(level, diff[i])) for i in range(nb_questions)]
# print(pattern)

"""pattern = [True, True, True, False, False, False]
asked = {1, 2, 3}"""

# X = diff
# y = pattern
# print(X, y)

def ll(theta):
    s = 0
    for j in asked:
        p = proba(theta, X[j])
        s += y[j] * log(p) + (1 - y[j]) * log(1 - p)
    return s

def dll(theta, history):
    s = 0
    for diff, outcome in history:
        p = proba(theta, diff)
        s += outcome * (1 - p) - (1 - outcome) * p
        # s += outcome - outcome * p - p + outcome * p
        # s += outcome - p
    return s

"""history = [(4, 1), (5, 0)]
for th in range(3, 8):
    print(th, dll(th, history))"""

def compute_level_est(history):
    fake_history = history[:]
    if all(not outcome for _, outcome in history):
        fake_history = history + [(-1, True)]
    if all(outcome for _, outcome in history):
        fake_history = history + [(8, False)]
    # return brentq(dll, 0, 7, history)
    # return brentq(dll, -2, 9, fake_history)
    mini = float('inf')
    best_v = None
    for i in range(-2, 16 + 1):
        v = i / 2
        fv = abs(dll(v, fake_history))
        if fv < mini:
            mini = fv
            best_v = v
    # print(fake_history, best_v)
    return best_v

"""
asked = set()
theta_est = 4
for step in range(1, 4):
    print('Tour', step)
    _, best = min((abs(proba(theta_est, diff[j]) - 0.5), j) for j in range(len(diff)))
    print('On pose', X[best])
    asked.add(best)
    print('Réponse', pattern[best])
    if step >= 2:
        theta_est = brentq(dll, 0, 7)
    else:
        theta_est = 6 if pattern[best] else 2
    print('Estimé', theta_est)

d = 1
est = 4
print('LL', list(ll(est + eps) for eps in np.linspace(d * (level - est), d * (est - level), num=10)))
print('DLL', list(dll(est + eps) for eps in np.linspace(d * (level - est), d * (est - level), num=10)))

est = brentq(dll, 0, 7)
print(est)
print(dll(est))
print('stop')
d = 1
print(list(ll(est + eps) for eps in np.linspace(d * (level - est), d * (est - level), num=10)))
print(ll(est))
print(ll(level))
"""
