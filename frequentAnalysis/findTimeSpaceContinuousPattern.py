#!/usr/bin/python
# -*- coding: utf-8 -*-
###吴施楷###

import sys
import re


PLACE_HOLDER = '_'


def read(filename):
    S = []
    with open(filename, 'r') as input:
        for line in input.readlines():
            elements = line.split(',')
            # print(elements)
            s = []
            for e in elements:
                s.append(e.split())
            S.append(s)
    return S

def number2string(input):
    data = []
    number = len(input)
    for i in range(number):
        s = ''
        squence = input[i]
        for j in range(len(squence)):
            s += str(squence[j])
        data.append(s)
    return data

    pass


class SquencePattern:

    def __init__(self, squence, support):
        self.squence = ''
        for s in squence:
            self.squence += str(s)
        self.support = support

    def append(self, p):
        #只关注原始序列
        self.squence += p.squence
        self.support = min(self.support, p.support)


def prefixSpan(pattern, S, threshold):
    #所有的频繁模式
    patterns = []
    f_list = frequent_items(S, pattern, threshold)

    for i in f_list:
        p = SquencePattern(pattern.squence, pattern.support)
        #单个模式
        p.append(i)
        #生成所有模式
        patterns.append(p)

        #投影子序列
        p_S = build_projected_database(S, p)
        #投影子模式
        p_patterns = prefixSpan(p, p_S, threshold)
        #模式叠加
        patterns.extend(p_patterns)

    return patterns


def frequent_items(S, pattern, threshold):
    items = {}
    _items = {}
    f_list = []
    if S is None or len(S) == 0:
        return []

    if len(pattern.squence) != 0:
        element = pattern.squence
    else:
        element = ''

    for s in S:
        alpha = set(s)
        for item in alpha:
            number = len(re.findall(element+item, element+s))
            if item in items:
                items[item] += number
            else:
                items[item] = number

    f_list.extend([SquencePattern([k], v)
                   for k, v in items.items()
                   if v >= threshold])
    sorted_list = sorted(f_list, key=lambda p: p.support)

    return sorted_list


def build_projected_database(S, pattern):

    p_S = []
    prefix = pattern.squence
    for s in S:
        p_s = []
        # s = s + prefix
        location = s.find(prefix[-1])
        if(location == -1):
            continue
        else:
            p_s = s[location+1:]

        if len(p_s) != 0:
                p_S.append(p_s)

    return p_S
    pass

def print_patterns(patterns):
    for p in patterns:
        print("pattern:{0}, support:{1}".format(p.squence, p.support))
    print(len(patterns))


if __name__ == "__main__":
    # S = read("Span2.txt")
    # S = [['a','c','b','a','b','c'],['a','d','c','a','b'],['a','b','b','a']]
    # S = [['a', 'c', 'b', 'a', 'b', 'b', 'a', 'b', 'c', 'a', 'b'], ['a', 'b', 'c'], ['a', 'b', 'b']]
    # S = [[4,3,4,0],[0,1,3,4,3,4,3,4,0],[3,1,3,4,0,4,3,4,0],[0,3,1,4,0,4,1,4],[0,3,0,4,0],[3,2,1,4,0],[0,1,4],[3,4,4,3,0]]
    S = [[3, 1, 2, 0, 4, 0, 4, 3, 4, 0], [0, 3, 1, 4, 0, 4, 1, 4]]
    S = number2string(S)
    print(S)
    patterns = prefixSpan(SquencePattern([], sys.maxsize), S, 2) #maxint -maxsize
    print_patterns(patterns)
