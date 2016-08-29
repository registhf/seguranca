import numpy as np

ceasar = np.vectorize(lambda x, k: (x + 256 + k) % 256)
deceasar = np.vectorize(lambda x, k: (x + 256 - k) % 256)