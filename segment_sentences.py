#!/usr/bin/python
# -*- coding: utf-8 -*-

import getopt
import sys
from Segment import Segment
from pro_dict import ProDict
from optparse import OptionParser


def interactive_mode(seg, operation):
    flag = True
    output = None
    if operation.out:
        output = open(operation.out, 'w')
    while flag:
        sen = raw_input('seg_sentence >>')
        if sen.lower() in ('q', 'quit', 'e', 'exit'):
            print 'Exit...'
            flag = False
        else:
            s = unicode(sen, 'utf-8')
            results = seg.segment([s.encode('utf-8'), ])
            for result in results:
                print result
            if output is not None:
                for result in results:
                    result = result.encode('utf-8')
                    output.write(result)
    if output is not None:
        output.close()
    sys.exit()


def segment_sentences():

    usage = '''
Usage of segment_sentences:
python segment_sentences.py [options] [arg]
Options and arguments:
-d, --debug            print the debug information of the segmentation, default is not
-f, --file [filename]  segment sentences from the specified file
-h, --help             display this help info and exit
-i, --interactive      go into interactive mode
-o, --out [filename]   write the segment result into the specified file
-s, --separator        specified the separator of the segmentation result
-t, --train [filename] use the training set to train the algorithm
-v, --version          output version info and exit
'''
    paser = OptionParser(usage)
    paser.version = 'Version.1.0'
    paser.add_option('-d', '--debug', action='store_true', dest='debug',
                     help='print the debug information of the segmentation, default is not')
    paser.add_option('-f', '--file', action='store', dest='file',
                     help='segment sentences from the specified file')
    paser.add_option('-i', '--interactive', action='store_true', dest='interactive',
                     help='go into interactive mode')
    paser.add_option('-o', '--out', action='store', dest='out',
                     help='write the segment result into the specified file')
    paser.add_option('-s', '--separator', action='store', dest='separator',
                     help='specified the separator of the segmentation result')
    paser.add_option('-t', '--train', action='store', dest='train',
                     help='use the training set to train the algorithm')
    paser.add_option('-v', '--version', action='store_true', dest='version',
                     help='output version info and exit')
    operation, arg = paser.parse_args(sys.argv)
    print operation.debug
    print operation.interactive
    print operation.file
    print operation.version
    print operation.train
    print operation.separator
    print operation.out
    pro_dic = None
    seg = Segment()
    if operation.train:
        train_set=open(operation.train)
        pro_dic=ProDict(train_set)
    else:
        pro_dic=ProDict()
    seg.pro_dictionary = pro_dic
    if operation.debug:
        seg.debug=True
    if operation.interactive:
        interactive_mode(seg, operation)
    else:
        if operation.file:
            print 'Read the input file...'
            input_file = open(operation.file)
            sens = input_file.readlines()
            input_file.close()
            print 'Start segment the input lines'
            results = seg.segment(sens)
            for result in results:
                print result
            #  write the result to the specified file
            print results
            if operation.out:
                write_result = open(operation.out, 'w')
                for result in results:
                    result = result.encode('utf-8')
                    write_result.write(result)
                write_result.close()

if __name__ == '__main__':
    segment_sentences()

