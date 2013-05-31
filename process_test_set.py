#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


def process_test_set(filename):
    f = open(filename, 'r')
    result_list = []
    alphabet = re.compile(ur'/[a-zA-Z]+')
    space = re.compile(r'  ')
    for line in f:
        l = unicode(line, 'gbk')
        l, num = alphabet.subn('', l)
        result_list.append(l)
    out_file = open('out_test_set.txt', 'w')
    # import ipdb; ipdb.set_trace()
    for l in result_list:
        out_file.write(l.encode('utf-8'))
    # out_file.writelines(result_list)
    f.close()
    out_file.close()
    in_list = []
    for line in result_list:
        l, num = space.subn('', line)
        in_list.append(l)
    in_file = open('in_test_set.txt', 'w')
    for l in in_list:
        in_file.write(l.encode('utf-8'))
    in_file.close()

if __name__ == '__main__':
    process_test_set('test_set.txt')
