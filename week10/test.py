from miller_rabin import miller_rabin
import numpy as np
from pretty_confusion_matrix import pp_matrix
from tqdm import tqdm
import pandas as pd
import os

dirname = os.path.dirname(__file__)
primes_path = os.path.join(dirname, 'primes.csv')

primes = set(np.genfromtxt(primes_path, delimiter=',', dtype=int)[1:, 1])

confusion_matrix = np.array([[0, 0], [0, 0]])

for i in tqdm(range(5, int(1e3), 2)):
    reality_prime = i in primes
    prediction_prime = miller_rabin(i, 20)

    confusion_matrix[int(reality_prime), int(prediction_prime)] += 1

cmap = 'PuRd'
pp_matrix(pd.DataFrame(confusion_matrix), cmap=cmap)