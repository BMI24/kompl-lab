from __future__ import annotations
from argparse import ArgumentParser
from typing import Iterable, Tuple, List
from itertools import product, chain

halt_states = ['halt', 'ja', 'nein']
movement_to_offset = {
    'L':-1,
    'N':0,
    'R':1
}
offset_to_movement = {
  -1:'L',
  0:'N',
  1:'R'
}

parser = ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('output_filename')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

transitions: dict[Tuple[str, Tuple[str]], Tuple[str, Tuple[str], Tuple[int]]] = dict()

lines = None
with open(args.input_file) as file:
    lines = [line.rstrip().lstrip() for line in file]

lines = [l for l in lines if not l.startswith('#') and l != '']

state_count, tape_count, alphabet_size, transitions_count = [int(s) for s in lines[0].split(' ')]
symbols : list[str] = [s.lstrip().rstrip() for s in lines[1].split(',')]
for line in lines[2:]:
    linesplit = [l.rstrip().lstrip() for l in  line.split(',')]
    q_old = linesplit[0]
    s_old = tuple(linesplit[1:1+tape_count])
    q_new = linesplit[1+tape_count]
    s_new = tuple(linesplit[2+tape_count::2])
    movement = tuple((movement_to_offset[m] for m in linesplit[3+tape_count::2]))
    transitions[(q_old, s_old)] = (q_new, s_new, movement)
original_states = set(chain((t[0][0] for t in transitions.items()), (t[1][0] for t in transitions.items())))
for halt_state in halt_states:
    if halt_state in original_states:
        original_states.remove(halt_state)


new_transitions: dict[Tuple[str, str], Tuple[str, str, int]] = dict()


# Phase 1: Übersetzung
# State t1_:
# State t2_:
# lese 1 Zeichen, gehe in Zustand der das Zeichen kodiert und gehe eins nach rechts (Schleife bis zum Ende)

first_state = '0'

for symbol in chain(symbols, '_'):
    new_transitions[('0', symbol)] = (f't1_{symbol}', 'S-'*tape_count, 1)
    for symbol2 in chain(symbols, '_'):
        new_transitions[(f't1_{symbol}', symbol2)] = (f't2_{symbol2}', f'{symbol}*' + '_*'*(tape_count - 1), 1)
        new_transitions[(f't2_{symbol}', symbol2)] = (f't2_{symbol2}', f'{symbol}-' + '_-'*(tape_count - 1), 1)
    new_transitions[(f't1_{symbol}', '_')] = (first_state + 'S', f'{symbol}*' + '_*' * (tape_count - 1), 1)
    new_transitions[(f't2_{symbol}', '_')] = (first_state + 'S', f'{symbol}-' + '_-' * (tape_count - 1), 1)

# Phase 2: Suche

def get_all_compressed_tape_contents(): 
    s = [s + '*' for s in symbols + ['_']] + [s + '-' for s in symbols + ['_']]
    return (''.join(s) for s in product(s, repeat=tape_count))

def get_all_start_variations():
    s = ['S-', 'S*']
    return (''.join(s) for s in product(s, repeat=tape_count))


# State S: goes to the beginning (to compressed start) of the compressed tape

for original_state in original_states:
    s_state_name = original_state + 'S'
    new_transitions[(s_state_name, '_')] = (s_state_name, '_', -1)
    for s in get_all_compressed_tape_contents():
        new_transitions[(s_state_name, s)] = (s_state_name, s, -1)

    for s in get_all_start_variations():
        # evil evil hack abusing that we named the previous state S -> 'S' + 'EARCH' = 'SEARCH
        new_transitions[(s_state_name, s)] = (s_state_name+'EARCH'+'_'*tape_count, s, 0)

# State {SIMULATED_STATE}SEARCH{SIMULATED_HEAD_CONTENT}:
#   fills {SIMULATED_HEAD_CONTENT} from compressed tape

def get_all_search_states():
    s = symbols + ['_']
    return (s for s in product(s, repeat=tape_count))

def find_char(str: str, ch: str) -> Iterable[int]:
    for i, ltr in enumerate(str):
        if ltr == ch:
            yield i

for original_state in original_states:
    for c in chain(get_all_compressed_tape_contents(), get_all_start_variations()):
        for s in get_all_search_states():
            prev_state = ''.join(chain(original_state, 'SEARCH', s))
            target_state_repr = list(s)
            for idx in find_char(c, '*'):
                target_state_repr[idx//2] = c[idx-1]
            new_state = ''.join(chain(original_state, 'SEARCH', target_state_repr))
            new_transitions[(prev_state, c)] = (new_state, c, 1)


# Phase 3: Änderung

# reaching _ on the tape marks end of compressed tape, go to relevant UPDATE state
# (directly sourced from the original transitions)
for transition in transitions.items():
    old_state = transition[0][0]
    expected_input = ''.join(transition[0][1])
    old_state = old_state + 'SEARCH' + expected_input
    if transition[1][0] == 'halt':
        new_state = 'DECOMPRESS_'
    elif transition[1][0] == 'ja':
        new_state = 'ja'
    elif transition[1][0] == 'nein':
        new_state = 'nein'
    else:
        new_state = transition[1][0] + 'LUPDATE' + ''.join(offset_to_movement[o] for o in  transition[1][2]) + ''.join(transition[1][1])
    new_transitions[(old_state, '_')] = (new_state, '_', -1)

def get_all_mov_instr_during_left_walk():
    # . is the marker for drop at the next cell
    # N does not need to be moved anymore
    s = ['L', 'R', '.', 'N']
    return product(s, repeat=tape_count)

def get_all_mov_instr_during_left_walk_boundary():
    # not possible anymore:
    # . (equal to left-move out of tape)
    # L (because we already replaced all of them)
    s = ['R', 'N']
    return product(s, repeat=tape_count)


def get_all_mov_instr_during_right_walk():
    # . is the marker for drop at the next cell
    # N does not need to be moved anymore
    s = ['R', '.', 'N']
    return product(s, repeat=tape_count)

def get_all_mov_instr_during_right_walk_boundary():
    s = ['.','N']
    return product(s, repeat=tape_count)

def get_all_substitutions():
    s = symbols + ['S', '_']
    return product(s, repeat=tape_count)


# left-walk: 
# - move all heads which should move to the left
# - replace tape contents in compressed tape

for original_state in original_states:
    for substitution in get_all_substitutions():
        for old_compressed_symbol in chain(get_all_compressed_tape_contents(), get_all_start_variations()):
            for old_mov_instr in get_all_mov_instr_during_left_walk():
                new_mov_instr = list(old_mov_instr)
                new_compressed_symbol = list(old_compressed_symbol)
                for idx in find_char(old_compressed_symbol, '*'):
                    new_compressed_symbol[idx - 1] = substitution[idx//2]
                    if old_mov_instr[idx//2] == 'L':
                        new_mov_instr[idx//2] = '.'
                        new_compressed_symbol[idx] = '-'
                for idx in find_char(''.join(old_mov_instr), '.'):
                    new_compressed_symbol[idx * 2 + 1] = '*'
                    new_mov_instr[idx] = 'N'

                old_state = original_state + 'LUPDATE' + ''.join(old_mov_instr) + ''.join(substitution)
                new_state = original_state + 'LUPDATE' + ''.join(new_mov_instr) + ''.join(substitution)
                new_transitions[(old_state, old_compressed_symbol)] = (new_state, ''.join(new_compressed_symbol), -1)

            for old_mov_instr in get_all_mov_instr_during_right_walk():
                new_mov_instr = list(old_mov_instr)
                new_compressed_symbol = list(old_compressed_symbol)
                for idx in find_char(old_compressed_symbol, '*'):
                    new_compressed_symbol[idx - 1] = substitution[idx//2]
                    if old_mov_instr[idx//2] == 'R':
                        new_mov_instr[idx//2] = '.'
                        new_compressed_symbol[idx] = '-'
                for idx in find_char(''.join(old_mov_instr), '.'):
                    new_compressed_symbol[idx * 2 + 1] = '*'
                    new_mov_instr[idx] = 'N'

                old_state = original_state + 'RUPDATE' + ''.join(old_mov_instr) + ''.join(substitution)
                new_state = original_state + 'RUPDATE' + ''.join(new_mov_instr) + ''.join(substitution)
                new_transitions[(old_state, old_compressed_symbol)] = (new_state, ''.join(new_compressed_symbol), 1)
        
        # left walk ending on uncompressed S
        for old_mov_instr in get_all_mov_instr_during_left_walk_boundary():
            old_state = original_state + 'LUPDATE' + ''.join(old_mov_instr) + ''.join(substitution)
            new_state = original_state + 'RUPDATE' + ''.join(old_mov_instr) + ''.join(substitution)
            new_transitions[(old_state, 'S')] = (new_state, 'S', 1)
        
        # extend tape to the right on demand
        for old_mov_instr in get_all_mov_instr_during_right_walk_boundary():
            old_state = original_state + 'RUPDATE' + ''.join(old_mov_instr) + ''.join(substitution)
            new_state = original_state + 'S'
            new_compressed_symbol = list('_-' * tape_count)
            for idx in find_char(''.join(old_mov_instr), '.'):
                new_compressed_symbol[idx * 2 + 1] = '*'
            new_transitions[(old_state, '_')] = (new_state, ''.join(new_compressed_symbol), 0)

        # ... but dont extend when not needed
        old_state = original_state + 'RUPDATE' + 'N' * tape_count + ''.join(substitution)
        new_state = original_state + 'S'
            
        new_transitions[(old_state, '_')] = (new_state, '_', -1)


# Phase 4: Rückübersetzung
# bei JA und NEIN ist der Bandinhalt egal
# die Kopfposition am Ende ist auch egal
# DECOMPRESS{SYMBOL} 
#   nimmt altes Symbol SYMBOL2 auf, platzert SYMBOL auf dem Band und geht in DECOMPRESS{SYMBOL2}

for old_compressed_symbol in chain(get_all_compressed_tape_contents(), get_all_start_variations()):
    for old_symbol in symbols + ['_', 'S']:
        for new_compressed_symbol in chain(get_all_compressed_tape_contents(), get_all_start_variations()):
            old_state = 'DECOMPRESS' + old_symbol
            new_state = 'DECOMPRESS'  + new_compressed_symbol[-2]
            
            new_transitions[(old_state, new_compressed_symbol)] = (new_state, old_symbol, -1)

new_transitions[('DECOMPRESSS', 'S')] = ('halt', 'S', 0)

with open(args.output_filename, 'w') as f:
  f.write('-1 1 -1 -1\n')
  f.write('todo\n')
  for transition in new_transitions.items():
    f.write(f"{transition[0][0]},{transition[0][1]},{transition[1][0]},{transition[1][1]},{offset_to_movement[transition[1][2]]}")

    f.write('\n')