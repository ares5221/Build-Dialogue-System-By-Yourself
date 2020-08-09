#!/usr/bin/env python
# _*_ coding:utf-8 _*_

def hamming_distance(str1, str2):
    '''
    Return the Hamming distance between equal-length sequences
    :param str1: 
    :param str2: 
    :return: 
    '''
    if len(str1) != len(str2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(str1, str2))


if __name__ == "__main__":
    str1 = 'abc'
    str2 = 'abd'
    hd = hamming_distance(str1, str2)
    print(hd)
