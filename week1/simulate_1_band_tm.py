from __future__ import annotations
from argparse import ArgumentParser
from typing import Tuple

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

transitions: dict[Tuple[str, str], Tuple[str, str, str]] = dict()

with open(args.filename) as f:
    state_count, transitions_count = [int(s) for s in f.readline().rstrip('\n').split(' ')]
    for _ in range(transitions_count):
        q_old, s_old, q_new, s_new, movement = f.readline().rstrip('\n').split(',')
        transitions[(q_old, s_old)] = (q_new, s_new, movement)

tape_content: list[str] = list("S" + args.input)
head_pos: int = 1
state: str = "0"

def print_info():
    print('Bandinhalt:')
    print(''.join(tape_content))
    print(' '*head_pos+'^')
    print('Zustand:', state)
    print()

while state not in halt_states:
    if args.verbose:
        print_info()
    
    transition = transitions.get((state, tape_content[head_pos]), None)
    if transition is None:
        state = "nein"
    else:
        q_new, s_new, movement = transition
        state = q_new

        tape_content[head_pos] = s_new
        head_pos += movement_to_offset[movement]

        if head_pos < 0:
            state = "nein"
        elif head_pos >= len(tape_content):
            tape_content.append('_')

print_info()
