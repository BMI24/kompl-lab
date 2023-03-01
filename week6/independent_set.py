from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set
from .literal_utils import add_clause, write_output, write_verbose_output, Literal, add_implication_clause, add_equivalence_clause

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

def count_grid(count : int, l : int) -> Literal:
    return Literal(f'count_grid_{count}_{l}')
def node_used(l : int) -> Literal:
    return Literal(f'node_used_{l}')


for edge in edges:
    #dont use edge[0] or dont use edge[1] 
    add_clause(-node_used(edge[0]), -node_used(edge[1]))

# add init clauses
add_equivalence_clause(count_grid(0,1), -node_used(1))
add_equivalence_clause(count_grid(1,1), node_used(1))

for l in range(k + 1):
    for i in range(1, vert_count + 1):
        if l == 0:
            add_clause(node_used(l), -count_grid(i, l-1), count_grid(i, l))
            add_clause(-count_grid(i,l), -node_used(l))
            add_clause(-count_grid(i, l), count_grid(i, l-1))
        else:
            add_clause(-node_used(l), -count_grid(i-1, l-1), count_grid(i, l))
            add_clause(node_used(l), -count_grid(i, l-1), count_grid(i,l))
            add_clause(count_grid(i, l-1), node_used(l), -count_grid(i,l))
            add_clause(-node_used(l), count_grid(i-1, l-1), -count_grid(i, l))
            add_clause(count_grid(i, l-1), count_grid(i-1, l-1), -count_grid(i, l))

add_clause(*(count_grid(i, k) for i in range(vert_count)))

write_output(args.output_path)
if (args.verbose_out):
    write_verbose_output(args.verbose_out)