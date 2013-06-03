#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

def segment_all(segment_file):
    f = open(segment_file)
    lines = f.readlines()
    f.close()
    lines_length = len(lines)
    line_list = []
    count = 0
    for line in lines:
        line = unicode(line, 'utf8')
        line_list.append(line)
        count += 1
        if (count % 5) == 0 or count == lines_length:
            in_file = open('input_sentence.txt', 'w')
            for l in line_list:
                in_file.write(l.encode('utf-8'))
            in_file.close()
            os.system('./segment_sentences.py -f input_sentence.txt -o result.txt')
            line_list = []
        import ipdb; ipdb.set_trace()
    print 'Success!'
    return True


if __name__ == '__main__':
    segment_all('in_test_set.txt')
