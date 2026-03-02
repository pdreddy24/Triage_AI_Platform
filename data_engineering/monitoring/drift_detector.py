import numpy as np


def detect_mean_shift(reference, current, threshold=0.2):
    ref_mean = np.mean(reference)
    cur_mean = np.mean(current)

    return abs(ref_mean - cur_mean) > threshold