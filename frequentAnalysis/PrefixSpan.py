#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys


PLACE_HOLDER = '_'


def read(filename):
    S = []
    with open(filename, 'r') as input:
        for line in input.readlines():
            elements = line.split(',')
            s = []
            for e in elements:
                s.append(e.split())
            S.append(s)
    # print(S)
    return S


class SquencePattern:
    def __init__(self, squence, support):
        #squence:单个样本 ['a', ['c', 'd'], 'b']
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
    patterns = []
    f_list = frequent_items(S, pattern, threshold)
    if(len(f_list)>0):
        print(len(f_list))
        print('ssssssss',(f_list[0].squence))

    for i in f_list:
        p = SquencePattern(pattern.squence, pattern.support)
        p.append(i)
        patterns.append(p)

        p_S = build_projected_database(S, p)
        p_patterns = prefixSpan(p, p_S, threshold)
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
        print(S)

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
            print(element)
            for item in element:
                print(item)
                if item not in counted:
                    counted.append(item)
                    if item in items:
                        items[item] += 1
                    else:
                        items[item] = 1
        print(items)
    #子序列取代
    f_list.extend([SquencePattern([[PLACE_HOLDER, k]], v)
                   for k, v in _items.items()
                   if v >= threshold])
    #相关序列
    f_list.extend([SquencePattern([[k]], v)
                   for k, v in items.items()
                   if v >= threshold])
    sorted_list = sorted(f_list, key=lambda p: p.support)
    return sorted_list


def build_projected_database(S, pattern):

    p_S = []
    last_e = pattern.squence[-1]
    last_item = last_e[-1]
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


if __name__ == "__main__":
    S = read("span1.txt")
    patterns = prefixSpan(SquencePattern([], sys.maxsize), S, 2)
    print_patterns(patterns)
