# taken from https://pysathq.github.io/
from argparse import ArgumentParser
from typing import List, Set
from pysat.formula import CNF
from pysat.solvers import Solver



parser = ArgumentParser()
parser.add_argument('input_file')
args = parser.parse_args()

# create a satisfiable CNF formula "(-x1 ∨ x2) ∧ (-x1 ∨ -x2)":
cnf = CNF(from_file=args.input_file)

# create a SAT solver for this formula:
with Solver(bootstrap_with=cnf) as solver:
    # 1.1 call the solver for this formula:
    print('formula is', f'{"s" if solver.solve() else "uns"}atisfiable')

    # 1.2 the formula is satisfiable and so has a model:
    print('and the model is:', solver.get_model())

    # 2.1 apply the MiniSat-like assumption interface:
    print('formula is',
        f'{"s" if solver.solve(assumptions=[1, 2]) else "uns"}atisfiable',
        'assuming x1 and x2')

    # 2.2 the formula is unsatisfiable,
    # i.e. an unsatisfiable core can be extracted:
    print('and the unsatisfiable core is:', solver.get_core())