#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys


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


class SquencePattern:
    def __init__(self, squence, support):
        self.squence = []
        for s in squence:
            self.squence.append(list(s))
        self.support = support

    def append(self, p):
        if p.squence[0][0] == PLACE_HOLDER:
            first_e = p.squence[0]
            first_e.remove(PLACE_HOLDER)
            self.squence[-1].extend(first_e)
            self.squence.extend(p.squence[1:])
        else:
            self.squence.extend(p.squence)
        self.support = min(self.support, p.support)


def prefixSpan(pattern, S, threshold):
    #所有的频繁模式
    patterns = []
    f_list = frequent_items(S, pattern, threshold)

    for i in f_list:
        p = SquencePattern(pattern.squence, pattern.support)
        p.append(i)
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
        last_e = pattern.squence[-1]
    else:
        last_e = []
    for s in S:

        #class 1
        is_prefix = True
        for item in last_e:
            if item not in s[0]:
                is_prefix = False
                break
        if is_prefix and len(last_e) > 0:
            index = s[0].index(last_e[-1])
            if index < len(s[0]) - 1:
                for item in s[0][index + 1:]:
                    if item in _items:
                        _items[item] += 1
                    else:
                        _items[item] = 1

        #class 2
        if PLACE_HOLDER in s[0]:
            for item in s[0][1:]:
                if item in _items:
                    _items[item] += 1
                else:
                    _items[item] = 1
            s = s[1:]

        #class 3
        counted = []
        for element in s:
            for item in element:
                if item not in counted:
                    counted.append(item)
                    if item in items:
                        items[item] += 1
                    else:
                        items[item] = 1
    #替换序列
    f_list.extend([SquencePattern([[PLACE_HOLDER, k]], v)
                   for k, v in _items.items() # iteritems
                   if v >= threshold])
    #保留序列
    f_list.extend([SquencePattern([[k]], v)
                   for k, v in items.items()
                   if v >= threshold])
    sorted_list = sorted(f_list, key=lambda p: p.support)
    return sorted_list


def build_projected_database(S, pattern):

    p_S = []
    last_e = pattern.squence[-1]
    last_item = last_e[-1]
    print('SSSSSS',S)
    print('last_e',last_e)
    for s in S:
        p_s = []
        for element in s:
            is_prefix = False
            if PLACE_HOLDER in element:
                if last_item in element and len(pattern.squence[-1]) > 1:
                    is_prefix = True
            else:
                is_prefix = True
                for item in last_e:
                    if item not in element:
                        is_prefix = False
                        break

            if is_prefix:
                e_index = s.index(element)
                i_index = element.index(last_item)
                if i_index == len(element) - 1:
                    p_s = s[e_index + 1:]
                else:
                    p_s = s[e_index:]
                    index = element.index(last_item)
                    e = element[i_index:]
                    e[0] = PLACE_HOLDER
                    p_s[0] = e
                break
        if len(p_s) != 0:
            p_S.append(p_s)

    return p_S


def print_patterns(patterns):
    for p in patterns:
        print("pattern:{0}, support:{1}".format(p.squence, p.support))
    print(len(patterns))


if __name__ == "__main__":
    S = read("Span2.txt")
    print(S)
    patterns = prefixSpan(SquencePattern([], sys.maxsize), S, 2) #maxint -maxsize
    print_patterns(patterns)
