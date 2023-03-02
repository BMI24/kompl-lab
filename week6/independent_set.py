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

def count_after_node(count : int, l : int) -> Literal:
    return Literal(f'count_grid_{count}_{l}')
def node_used(l : int) -> Literal:
    return Literal(f'node_used_{l}')


for edge in edges:
    #dont use edge[0] or dont use edge[1] 
    add_clause(-node_used(edge[0]), -node_used(edge[1]))

# add init clauses
add_equivalence_clause(count_after_node(0, 1), -node_used(1))
add_equivalence_clause(count_after_node(1, 1), node_used(1))

for c in range(k + 1):
    for n in range(1, vert_count + 1):
        if c == 0:
            # count_after_node(c, n) -> -(count_after_node(c, n - 1) & node_used(n))
            # = -count_after_node(c, n) | -count_after_node(c, n - 1) | -node_used(n)
            add_clause(-count_after_node(n, c), -count_after_node(c, n - 1), -node_used(n))
        else:
            # count_after_node(c, n) <-> (node_used(n) & count_after_node(c - 1, n - 1)) | (-node_used(n) & count_after_node(c, n - 1))
            # = (-node_used(n) | -count_after_node(c - 1, n - 1) | count_after_node(c, n) 
            #  & (node_used(n) | -count_after_node(c, n - 1) | count_after_node(c, n) 
            #  & (count_after_node(c, n - 1) | node_used(n) | -count_after_node(c, n) 
            #  & (-node_used(n) | count_after_node(c - 1, n - 1) | -count_after_node(c, n) 
            #  & (count_after_node(c, n - 1) | count_after_node(c - 1, n - 1) | -count_after_node(c, n) 
            add_clause(-node_used(n), -count_after_node(c-1, n-1), count_after_node(c, n))
            add_clause(node_used(n), -count_after_node(c, n-1), count_after_node(c,n))
            add_clause(count_after_node(c, n-1), node_used(n), -count_after_node(c,n))
            add_clause(-node_used(n), count_after_node(c-1, n-1), -count_after_node(c, n))
            add_clause(count_after_node(c, n-1), count_after_node(c-1, n-1), -count_after_node(c, n))

for c in range(2, k + 1):
    add_clause(-count_after_node(c, 0))
add_clause(*(count_after_node(k, n) for n in range(1, vert_count + 1)))

write_output(args.output_path)
if (args.verbose_out):
    write_verbose_output(args.verbose_out)