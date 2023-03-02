from __future__ import annotations
from argparse import ArgumentParser
from typing import List, Set, Tuple
import numpy as np

def miller_rabin(n : int, k : int) -> bool:
    assert(n%2 != 0)

    d = n - 1
    s = 0
    while d % 2 == 0:
        d = d // 2
        s += 1

    for _ in range(k):
        a = np.random.randint(2, n-1)
        x = pow(a, d, n)
        if x == 1:
            return True
        for _ in range(s):
            if x % n == n - 1:
                return True
            else:
                x = pow(x, 2, n)
    return False

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('n')
    parser.add_argument('k')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    n = int(args.n)
    k = int(args.k)
    print(miller_rabin(n, k))