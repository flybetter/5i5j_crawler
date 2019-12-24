import sys
import numpy as np


def begin():
    a = input("input a:")

    score = a.split(",")
    score = list(map(lambda x: int(x), score))
    avg = np.mean(score)
    print(avg)


if __name__ == '__main__':
    begin()
