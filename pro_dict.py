#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

class ProDict(object):
    ''' Get train set for tokenization. '''
    dict_file = ''

    def __init__(self, train_file):
        self.train_file = train_file
        self.construct_pro_dict()

    def is_vocable(self, vocable):
        if vocable in self.pro_dict:
            return True
        else:
            return False

    def preprocess_train_file(self, train_file):
        f = file(train_file)
        lines = f.readlines()
        f.close()
        for i in range(len(lines)):
            lines[i] = 's  ' + lines[i][0:-2] + ' e ' + lines[i][-1]
        return lines

    def construct_pro_dict(self):
        f = file(self.train_file)
        lines = f.readlines()
        f.close()
        re_han = re.compile(ur'([\u4E00-\u9FA5\s]+)')
        re_skip = re.compile(ur'([\.0-9]+|[a-zA-Z0-9]+)')
        re_eng = re.compile(ur'[a-zA-Z0-9]+')
        re_num = re.compile(ur'[\.0-9]+')
        all_words = []
        sen_words = []
        for line in lines:
            sentences = re_han.split(line.strip(' '))
            length = len(sentences)
            for i in range(length):
                sentences[i] = 's  ' + sentences[i] + 'e'
            for s in sentences:
                words = s.split('  ')
                sen_words.append(words)
                all_words.extend(words)



if __name__ == '__main__':
    d = ProDict('train_seg.txt')
