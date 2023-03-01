from argparse import ArgumentParser
from typing import List, Set
import sys
from week6.literal_utils import add_clause, write_output, write_verbose_output, Literal, add_implication_clause

parser = ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-s', '--verbose_out')
parser.add_argument('output_path')
args = parser.parse_args()

with open(args.input_file) as file:
    lines = [line.rstrip().lstrip() for line in file]

n = int(lines[0])
sets : List[Set[int]] = [{int(x) for x in line.split(' ')} for line in lines[1:]]

def element_used_by_set(i : int, j : int) -> Literal:
    return Literal(f'set_element_used_{i},{j}')
def set_used(i : int) -> Literal:
    return Literal(f'set_used_{i}')

set_count = len(sets)
# prevent impossible association of elements with sets
for i in range(set_count):
    for j in sets[i].difference(range(n)):
        add_clause(-element_used_by_set(i,j))

for i in range(set_count):
    for j in sets[i].intersection(range(n)):
        # set element used -> whole set is used
        add_implication_clause(element_used_by_set(i, j), set_used(i))
        # if an element of a set is used -> the set is used
        add_implication_clause(set_used(i), element_used_by_set(i, j))

# each element needs to be used
for i in range(n):
    add_clause(*(element_used_by_set(j,i) for j in range(set_count)))

# a element can not be used by two sets at the same time
for i in range(set_count):
    for j in range(n):
        for k in range(i + 1, set_count):
            add_implication_clause(element_used_by_set(i,j), -element_used_by_set(k,j))

write_output(args.output_path)
if (args.verbose_out):
    write_verbose_output(args.verbose_out)