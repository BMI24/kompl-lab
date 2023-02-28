from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set

parser = ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('output_filename')
parser.add_argument('k')
args = parser.parse_args()

k = int(args.k)

# read graph

with open(args.input_file) as file:
    lines = [line.rstrip().lstrip() for line in file]

lines = [l for l in lines]

vert_count = int(lines[0])
edges = [tuple(int(v) for v in edge_str.split('-')) for edge_str in lines[1].split(' ')]

var_to_id : dict[str, int] = dict()
def id(name: str) -> int:
    id = var_to_id.get(name, None)
    if id is None:
        id = len(var_to_id) + 1
        var_to_id[name] = id
    return id


lines: List[str]= []
def add_clause_ids(clauses : List[int]):
    lines.append(' '.join(str(c) for c in clauses))

def parse_clause_str(clause : str):
    sign = 1
    if clause[0] == '-':
        clause = clause[1:]
        sign = -1
    return id(clause) * sign

def add_clause_str(*clauses : str):
    add_clause_ids([parse_clause_str(c) for c in clauses])

class Clause:
    def __init__(self, repr : str, neg : bool = False) -> None:
        self.negative : bool = neg
        self.representation : str = repr
    
    def __neg__(self) -> Clause:
        return Clause(self.representation, not self.negative)
    
    def __str__(self) -> str:
        return ('-' if self.negative else '') + self.representation
    
    def __repr__(self) -> str:
        return str(self)

def add_clause(*clauses : Clause):
    add_clause_str(*(str(c) for c in clauses))

# add edge clauses
for edge in edges:
    add_clause_str(f'-y{edge[0]}', f'-y{edge[1]}')

def x(i : int, l : int) -> Clause:
    return Clause(f'x{i},{l}')
def y(l : int) -> Clause:
    return Clause(f'y{l}')

# add init clauses
add_clause(-x(0, 1), -y(1))
add_clause(x(0,1), y(1))
add_clause(-x(1,1), y(1))
add_clause(-y(1), x(1,1))

for l in range(k):
    for i in range(vert_count):
        if l == 0:
            add_clause(y(l), -x(i, l-1), x(i, l))
            add_clause(-x(i,l), -y(l))
            add_clause(-x(i, l), x(i, l-1))
        else:
            add_clause(-y(l), -x(i-1, l-1), x(i, l))
            add_clause(y(l), -x(i, l-1), x(i,l))
            add_clause(x(i, l-1), y(l), -x(i,l))
            add_clause(-y(l), x(i-1, l-1), -x(i, l))
            add_clause(x(i, l-1), x(i-1, l-1), -x(i, l))

add_clause(*(x(k, i) for i in range(vert_count)))


with open(args.output_filename, 'w') as f:
    f.write(f'p cnf {len(var_to_id)} {len(lines)}\n')
    for line in lines:
        f.write(line)
        f.write('\n')