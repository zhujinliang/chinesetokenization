#!/usr/bin/python
# -*- coding: utf-8 -*-

import getopt
import sys
from Segment import Segment
from pro_dict import ProDict


def interactive_mode():
    flag = True
    while flag:
        sen = raw_input('seg_sentence>>')
        if sen == 'q':
            flag = False
        else:
            seg = Segment()
            pro_dic = ProDict()
            seg.pro_dictionary = pro_dic
            seg.segment(sen)
    sys.exit()


def segment_sentences():

    usage = '''
Usage of segment_sentences:
python segment_sentences.py [options] [arg]
Options and arguments:
-i, --interactive    go into interactive mode
-f, --file [filename] segment sentences from the specified file
-t, --train [filename] use the train set to train the algorithm
-h, --help           display this help info and exit
-v, --version        output version info and exit
'''
    version_info = 'Version 1.0'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hif:t:v', ['help', 'interactive', 'file', 'train', 'version'])
    except getopt.GetoptError as err:
        print usage
        sys.exit(2)
    for o, a in opts:
        if o in  ('-v', '--version'):
            print version_info
        elif o in ('-h', '--help'):
            print usage
        elif o in ('-i', '--interactive'):
            print 'Interactive Mode'
            interactive_mode()
        elif o in ('-f', '--file'):
            input_file = open(a)
            sens = input_file.readlines()
            seg = Segment()
            pro_dic = ProDict()
            seg.pro_dictionary = pro_dic
            seg.segment(sens)
        elif o in ('-t', '--train'):
            train_file = a
            ProDict(train_file)
            print 'Train successfully!'
        else:
            print usage
            sys.exit()
    if not opts:
        print usage
        sys.exit()

if __name__ == '__main__':
    segment_sentences()

