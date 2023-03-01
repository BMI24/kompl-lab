from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set, Dict, Union, Tuple, Optional, Generator
from enum import Enum
from copy import deepcopy

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
  EXISTS = 0
  ALL = 1

EXISTS = quantor_enum.EXISTS
ALL = quantor_enum.ALL


char_to_quantor = {'a' : ALL, 'e' : EXISTS}
atom_quantifier : Dict[int, quantor_enum] = dict()
def get_quantifier(literal : Literal):
    return atom_quantifier[abs(literal)]

atom_level : Dict[int, int] = dict()

def get_level(literal : Literal):
    return atom_level[abs(literal)]

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
        atom_quantifier[c] = quantor
        atom_level[c] = line_number
    
lines = lines[line_number:]

clauses = [{int(l) for l in filter(None, l[:-1].split(' '))} for l in lines]

def is_literal_used(literal : Literal, clauses : Clauses):
    return any(any(l == literal for l in clause) for clause in clauses)

def get_quantified_literals_above_level(level : int, quantor : quantor_enum):
    for atom in range(1, var_count + 1):
        if atom_quantifier[atom] == quantor and atom_level[atom] > level:
            yield atom

def get_used_atoms_above_level(level : int, quantor : quantor_enum, clauses : Clauses) -> Generator[Literal, None, None]:
    for atom in get_quantified_literals_above_level(level, quantor):
        if is_literal_used(atom, clauses) or is_literal_used(-atom, clauses):
            yield atom

def is_unit(literal : Literal, clauses : Clauses) -> bool:
    if get_quantifier(literal) != EXISTS:
        return False
    relevant_clauses = (clause for clause in clauses if literal in clause)
    if not any(all(l == literal or get_quantifier(l) == ALL for l in clause) for clause in relevant_clauses):
       return False
    if any(get_used_atoms_above_level(get_level(literal), ALL, clauses)):
        return False
    
    return True

def is_monoton(literal : Literal, clauses : Clauses) -> bool:
    if get_quantifier(literal) == EXISTS:
        return is_literal_used(literal, clauses) and not is_literal_used(-literal, clauses)
    if get_quantifier(literal) == ALL:
        return is_literal_used(-literal, clauses) and not is_literal_used(literal, clauses)
    raise NotImplementedError

def update_clauses(clauses : Clauses, atom : Literal, set_to_true : bool) -> Clauses:
    clauses = deepcopy(clauses)
    satisfied_clauses = []
    for clause in clauses:
        if atom in clause:
            if set_to_true:
                satisfied_clauses.append(clause)
            else:
                clause.remove(atom)
        if -atom in clause:
            if set_to_true:
                clause.remove(-atom)
            else:
                satisfied_clauses.append(clause)

    for clause in satisfied_clauses:
        clauses.remove(clause)
    return clauses

def qdpll(clauses: Clauses) -> bool:
    if len(clauses) == 0:
        return True
    if any(len(clause) == 0 for clause in clauses):
        return False
    
    for literal in (literal for clause in clauses for literal in clause):
        if is_unit(literal, clauses) or is_monoton(literal, clauses):
            return qdpll(update_clauses(clauses, abs(literal), literal > 0))
    
    important_ALL = min(list(get_used_atoms_above_level(-1, ALL, clauses)), key= lambda l: get_level(l), default=None)
    important_EXISTS = min(list(get_used_atoms_above_level(-1, EXISTS, clauses)), key= lambda l: get_level(l), default=None)
    if important_ALL is None:
        Q = EXISTS
    elif important_EXISTS is None:
        Q = ALL
    else:
        Q = ALL if get_level(important_ALL) < get_level(important_EXISTS) else EXISTS

    
    if Q == ALL:
        assert(important_ALL is not None)
        return qdpll(update_clauses(clauses, important_ALL, True)) and qdpll(update_clauses(clauses, important_ALL, False))
    else:
        assert(important_EXISTS is not None)
        return qdpll(update_clauses(clauses, important_EXISTS, True)) or qdpll(update_clauses(clauses, important_EXISTS, False))

print(qdpll(clauses))

