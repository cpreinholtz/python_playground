#!/usr/bin/env python
import numpy as np


def main():
    print('hello,  this program proves that probability for getting all tails in  mutiple flips is (probOfSingleTails)^nFlips')

    print("i.e. (1/2)^1 for one flip, 1/2^5 for 5 flips etc")

    #imagine a coin that is weighted, normal coin would be 0.5
    probHeads = 0.5

    nflips = 5
    nCases = 66666

    r = np.random.rand(nCases,nflips)
    print("heads")
    print(r)

    h=r<probHeads
    print("heads = True")
    print(h)

    s = np.sum(h,1)
    print("num heads per case")
    print(s)

    #arranged = np.arange(nflips)
    results = np.bincount(s)


    print("results are show as number of cases with [0 heads, 1 heads, ... )")
    print(results)


    print("final probability")
    print(results/nCases)


if __name__ == '__main__':
    main()
