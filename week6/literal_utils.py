from typing import List

var_to_id : dict[str, int] = dict()
def id(name: str) -> int:
    id = var_to_id.get(name, None)
    if id is None:
        id = len(var_to_id) + 1
        var_to_id[name] = id
    return id

out_lines : List[str] = []
out_verbose_lines : List[str] = []

def add_literal_ids(literals : List[int]):
    out_lines.append(' '.join(str(c) for c in literals + [0]))

def parse_literal_str(literal : str):
    sign = 1
    if literal[0] == '-':
        literal = literal[1:]
        sign = -1
    return id(literal) * sign

def add_clause_str(*literals : str):
    add_literal_ids([parse_literal_str(c) for c in literals])
    out_verbose_lines.append(' '.join(literals))

class Literal:
    def __init__(self, repr : str, neg : bool = False) -> None:
        self.negative : bool = neg
        self.representation : str = repr

    def __neg__(self): 
        return Literal(self.representation, not self.negative)
    
    def __str__(self) -> str:
        return ('-' if self.negative else '') + self.representation
    
    def __repr__(self) -> str:
        return str(self)

def add_clause(*literals : Literal):
    add_clause_str(*(str(c) for c in literals))

def add_implication_clause(reason : Literal, *implied : Literal):
    add_clause(*([-reason] + [l for l in implied]))

def add_equivalence_clause(left : Literal, right : Literal):
    add_implication_clause(left, right)
    add_implication_clause(right, left)

def write_output(path : str):
    with open(path, 'w') as f:
        f.write(f'p cnf {len(var_to_id)} {len(out_lines)}\n')
        for line in out_lines:
            f.write(line)
            f.write('\n')

def write_verbose_output(path : str):
    with open(path, 'w') as f:
        f.write(f'p cnf {len(var_to_id)} {len(out_lines)}\n')
        for line in out_verbose_lines:
            f.write(line)
            f.write('\n')