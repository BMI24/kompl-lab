from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set

parser = ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

var_count : int
clause_count : int

Literal = int
Clause = Set[Literal]
clauses : List[Clause] = list()

lines = None
with open(args.input_file) as file:
    lines = [line.rstrip().lstrip() for line in file]

lines = [l for l in lines if not l.startswith('c') and l != '']

# read DIMACS
# first line should be: p cnf <#variables> <#clauses>
var_count, clause_count = [int(s) for s in lines[0].split(' ')[-2:]]
for clause_line in lines[1:]:
    # each line after that eg: 
    # 1 -1 2 3 -5 0
    # skip last one (DIMACS defines each clause-line ends with a 0)
    clause = {int(l) for l in filter(None, clause_line[:-1].split(' '))}
    for literal in clause:
        # if the clause contains both the negative and positive literal, the clause is always SAT
        if -literal in clause:
            continue
    
    clauses.append(clause)

# none = not trivialy sat
def is_clause_trivialy_satisfiable(clause : Clause, partial_interpretation : Set[Literal]) -> bool | None:
    if len(clause & partial_interpretation) > 0:
        return True
    neg_interpretation : Set[Literal] = {-l for l in partial_interpretation}
    if len(clause - neg_interpretation) == 0:
        return False
    return None


# none = not trivialy sat
def is_trivialy_satisfiable(clauses : List[Clause], partial_interpretation : Set[Literal]) -> bool | None:
    for clause in clauses:
        clause_sat = is_clause_trivialy_satisfiable(clause, partial_interpretation)
        if not clause_sat:
            #print('not t sat: ', clause, partial_interpretation, clause_sat)
            return clause_sat
    
    # if we reach the end, each clause is trivialy sat
    return True

def dpll(clauses : List[Clause]) -> bool:
    sat = dpll_body(clauses, set())
    if sat is None:
        raise Exception
    return sat

def dpll_body(clauses : List[Clause], partial_interpretation : set[Literal]) -> bool | None:
    sat = is_trivialy_satisfiable(clauses, partial_interpretation)
    if sat is not None:
        return sat
    
    return (dpll_body(clauses, partial_interpretation | {len(partial_interpretation) + 1})
        or dpll_body(clauses, partial_interpretation | {-(len(partial_interpretation) + 1)}))

print(dpll(clauses))
#print(is_trivialy_satisfiable(clauses, {1, 3}))

    