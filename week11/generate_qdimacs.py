from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set, Dict
from enum import Enum
from numpy.random import randint, default_rng

parser = ArgumentParser()
parser.add_argument('-n', '--nodes', default=15, type=int)
parser.add_argument('-c', '--clauses', default=6, type=int)
parser.add_argument('-l', '--literals', default=4, type=int)
parser.add_argument('output_path')
args = parser.parse_args()

Literal = int
Clause = Set[Literal]
Clauses = List[Clause]
clauses : Clauses = list()

class quantor_enum(Enum):
  EXISTS = 0
  ALL = 1
quantor_to_char = { quantor_enum.ALL : 'a', quantor_enum.EXISTS : 'e' }

while True:
    literal_level : Dict[Literal, int] = {i : default_rng().poisson(2) for i in range(1, args.nodes + 1)}
    max_level = max(v for v in literal_level.values()) + 1
    first_quantifier = randint(0, 2)
    literal_quantifier : Dict[int, quantor_enum] = {i : quantor_enum(int(literal_level[i] % 2 == first_quantifier)) for i in range(1, args.nodes + 1)}

    all_levels_filled = True
    for level in range(max_level):
       all_levels_filled &= any(k for k, v in literal_level.items() if v == level)
    if not all_levels_filled:
       continue
    break

while len(clauses) < args.clauses:
    literals = default_rng().choice(args.nodes, args.literals, False) + 1
    all_existential = all(literal_quantifier[l] == quantor_enum.EXISTS for l in literals)
    if all_existential:
       continue
    literals[default_rng().choice(a=[False, True], size=(args.literals))] *= -1
    clauses.append(set(literals))





with open(args.output_path, 'w') as f:
    f.write(f'p cnf {args.nodes} {len(clauses)}\n')
    for level in range(max_level):
       level_clauses = [k for k, v in literal_level.items() if v == level]
       f.write(quantor_to_char[literal_quantifier[level_clauses[0]]] + ' ')
       f.write(' '.join(str(x) for x in level_clauses + [0]))
       f.write('\n')

    for clause in clauses:
        f.write(' '.join(str(l) for l in clause))
        f.write(' 0\n')