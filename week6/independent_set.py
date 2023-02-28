from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set

parser = ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('output_filename')
parser.add_argument('k')
args = parser.parse_args()

k = int(args.k)

# read graph

with open(args.input_file) as file:
    lines = [line.rstrip().lstrip() for line in file]

lines = [l for l in lines]

vert_count = int(lines[0])
edges = [tuple(int(v) for v in edge_str.split('-')) for edge_str in lines[1].split(' ')]

# ugh