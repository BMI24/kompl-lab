from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set, Dict, Union
from enum import Enum

parser = ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

var_count : int
clause_count : int

Literal = int
Clause = Set[Literal]
Clauses = List[Clause]
clauses : Clauses = list()

class quantor_enum(Enum):
  EXISTS = 0,
  ALL = 1

EXISTS = quantor_enum.EXISTS
ALL = quantor_enum.ALL


char_to_quantor = {'a' : ALL, 'e' : EXISTS}
literal_quantifier : Dict[int, quantor_enum] = dict()
literal_level : Dict[int, int] = dict()

lines = None
with open(args.input_file) as file:
    lines = [line.rstrip().lstrip() for line in file]

lines = [l for l in lines if not l.startswith('c') and l != '']

# read QDIMACS
# first line should be: p cnf <#variables> <#clauses>
var_count, clause_count = [int(s) for s in lines[0].split(' ')[-2:]]
lines = lines[1:]
line_number = 0
for line_number, line in enumerate(lines):
    # lines after that eg
    # e 1 4 3 8 0
    # a 2 5 0
    # e 1

    if not line.startswith(('e', 'a')):
        break
    
    # skip last one (DIMACS defines each clause-line ends with a 0)
    
    quantor = char_to_quantor[line[0]]

    quantified_variable = {int(l) for l in filter(None, line[2:-1].split(' '))}

    for c in quantified_variable:
        literal_quantifier[c] = quantor
        literal_level[c] = line_number
    
lines = lines[line_number:]

clauses = [{int(l) for l in filter(None, l[:-1].split(' '))} for l in lines]

def qdpll(clauses: Clauses) -> bool:
    if len(clauses) == 0:
        return True
    if any(len(clause) == 0 for clause in clauses):
        return False
    
    
