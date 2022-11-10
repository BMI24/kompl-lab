from __future__ import annotations
from argparse import ArgumentParser
from typing import Tuple, List

halt_states = ['halt', 'ja', 'nein']
movement_to_offset = {
    'L':-1,
    'N':0,
    'R':1
}

parser = ArgumentParser()
parser.add_argument('filename')
parser.add_argument('input')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

transitions: dict[Tuple[str, Tuple[str]], Tuple[str, Tuple[str], Tuple[int]]] = dict()

lines = None
with open(args.filename) as file:
    lines = [line.rstrip().lstrip() for line in file]

state_count, tape_count, alphabet_size, transitions_count = [int(s) for s in lines[0].split(' ')]
for line in lines[1:]:
    if line.startswith('#'):
        continue
    
    linesplit = line.split(',')
    q_old = linesplit[0]
    s_old = tuple(linesplit[1:1+tape_count])
    q_new = linesplit[2+tape_count]
    s_new = tuple(linesplit[3+tape_count:3+2*tape_count])
    movement = movement_to_offset[linesplit[-1]]
    transitions[(q_old, s_old)] = (q_new, s_new, movement)

tape_content: list[list[str]] = [list("S") if i > 0 else list('S'+ args.input) for i in range(tape_count)]
head_pos: list[int] = [1 for _ in range(tape_count)]
state: str = "0"

def print_info():
    print('-----------------------------')
    for i in range(tape_count):
        print(f'Bandinhalt {i + 1}:')
        print(''.join(tape_content[i]))
        print(' '*head_pos[i]+'^')
    print('Zustand:', state)
    print('-----------------------------')

while state not in halt_states:
    if args.verbose:
        print_info()
    
    transition : Tuple[str, Tuple[str], Tuple[int]] = transitions.get(state, tuple([tape_content[i][head_pos[i]] for i in range(tape_count)]), None)
    if transition is None:
        state = "nein"
    else:
        q_new, s_new, movement = transition
        state = q_new

        for i in range(tape_count):
            tape_content[i][head_pos[i]] = s_new[i]
            head_pos[i] += movement_to_offset[movement]

            if head_pos[i] < 0:
                state = "nein"
            elif head_pos[i] >= len(tape_content[i]):
                tape_content[i].append('_')

print_info()
