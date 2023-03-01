from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set
from literal_utils import add_clause, write_output, write_verbose_output, Literal

parser = ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-s', '--verbose_out')
parser.add_argument('output_path')
parser.add_argument('k')
args = parser.parse_args()

k = int(args.k)

# read graph

with open(args.input_file) as file:
    lines = [line.rstrip().lstrip() for line in file]

vert_count = int(lines[0])
edges = [tuple(int(v) for v in edge_str.split('-')) for edge_str in lines[1].split(' ')]

def x(i : int, l : int) -> Literal:
    return Literal(f'x{i},{l}')
def y(l : int) -> Literal:
    return Literal(f'y{l}')


# add edge clauses
for edge in edges:
    add_clause(-y(edge[0]), -y(edge[1]))

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

write_output(args.output_path)
if (args.verbose_out):
    write_verbose_output(args.verbose_out)