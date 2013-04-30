#!/usr/bin/python
# -*- coding: utf-8 -*-


class ProDict(object):
    ''' Get train set for tokenization. '''
    dict_file = ''

    def __init__(self, train_file):
        self.train_file = train_file

    def is_vocable(self, vocable):
        if vocable in self.pro_dict:
            return True
        else:
            return False
    
    def construct_pro_dict(self):
        f = file(self.train_file)
        sentences = f.readlines()
        f.close()
        all_words = []
        for s in sentences:
            words = s.split('  ')
            all_words.append(words)



if __name__ == '__main__':
    d = ProDict('p_train_seg.txt')
