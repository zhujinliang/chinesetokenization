#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import cPickle
import os

class ProDict(object):
    ''' Get train set for tokenization. '''
    dict_file = ''

    def __init__(self, train_file=None):
        self.train_file = train_file
        self.pro_dict = self._get_pro_dict()
        self.prefix_dict = self._get_prefix_dict()
        self.longest_length = self.get_longest_length_of_vocable()

    def has_vocable(self, vocable):
        if vocable in self.pro_dict:
            return True
        else:
            return False

    def get_longest_length(self):
        return self.longest_length

    def get_longest_length_of_vocable(self):
        length = 0
        for k in self.pro_dict:
            if len(k) > length:
                length = len(k)
        return length

    def get_tree_token_count(self,cur,pre1,pre2):
        # print cur
        # print pre1
        # print pre2

        if pre2 is None:
            prefix = 's_e'
        elif pre2 == 's':
            pre2 = 's_e'
            prefix = pre1 + '_' + pre2
        else:
            prefix = pre1 + '_' + pre2
        if self.pro_dict.has_key(cur):
            if self.pro_dict[cur].has_key(prefix):
                return self.pro_dict[cur][prefix]
            else:
                return 0.1
        else:
            return 0.1

    def get_pre_count(self,pre1,pre2):
        if pre2 is None:
            prefix = 's_e'
        elif pre2 == 's':
            pre2 = 's_e'
            prefix = pre1 + '_' + pre2
        else:
            prefix = pre1 + '_' + pre2
        if self.prefix_dict.has_key(prefix):
            return self.prefix_dict[prefix]
        else:
            count = 0
            amount = 0
            for(k,v) in self.pro_dict.items():
                if v.has_key(pre2):
                    count += 1
                    amount += v[pre2]
            if amount == 0:
                if self.pro_dict.has_key(pre1):
                    for (k,v) in self.pro_dict[pre1].items():
                        amount += v
                else:
                    amount = 100000
            amount += 0.1 * count
            return amount

    def get_pro(self, cur, pre1, pre2):
        three_token_count = self.get_tree_token_count(cur,pre1,pre2)
        pre_token_count = self.get_pre_count(pre1,pre2)
        pre_token_count = float(pre_token_count)
        three_token_count = float(three_token_count)

        # print 'pre_count '+pre_token_count.__str__()
        # print 'three_count '+three_token_count.__str__()
        pro = three_token_count * 1.0 / (pre_token_count * 1.0)
        # print pro

        return pro


    def _get_short_sen(self):
        # short_sen contains many small sentences string in list.
        short_sen = []
        
        f = open(self.train_file)
        lines = f.readlines()
        f.close()
        re_han = re.compile(ur'([\u4E00-\u9FA5]+)')
        re_biaodian = re.compile(ur'[\u2014-\u2026\u3000-\u303F\uff01-\uff0c\uff1a-\uff1f]')
        for line in lines:
            # Use unicode encode
            line = unicode(line, 'utf-8')
            sentences = re_biaodian.split(line.strip(' '))
            for s in sentences:
                if not s in ('', ' ', '  ', '\n', ' \n', '  \n'):
                    if s.startswith('  '):
                        s = 's' + s
                    else:
                        s = 's  ' + s
                    if s.endswith('\n'):
                        s = s[0:-1] + 'e'
                    if s.endswith('  '):
                        s = s + 'e'
                    else:
                        s = s + '  e'
                    short_sen.append(s)
        return short_sen

    def _get_sen_words(self):
        sen_words = []
        sen_words_file_name = 'sen_words.txt'
        short_sen = self._get_short_sen()
        for s in short_sen:
            words = s.split('  ')
            sen_words.append(words)
        if not os.path.exists(sen_words_file_name):
            sen_words_file = open(sen_words_file_name, 'w')
        else:
            sen_words_file = open(sen_words_file_name, 'r')
            old_sen_words = cPickle.load(sen_words_file)
            sen_words_file.close()
            sen_words.extend(old_sen_words)
            sen_words_file = open(sen_words_file_name, 'w')
        cPickle.dump(sen_words, sen_words_file)
        sen_words_file.close()
        return sen_words

    def _get_pro_dict(self):
        pro_dict = {}
        pro_dict_file_name = 'pro_dict.txt'
        if self.train_file is None:
            if os.path.exists(pro_dict_file_name):
                pro_dict_file = open(pro_dict_file_name, 'r')
                pro_dict = cPickle.load(pro_dict_file)
            else:
                print 'Not found the pro_dict.txt'
                return None
        else:
            sen_words = self._get_sen_words()
            for s in sen_words:
                for w in s:
                    if w in ['s', 'e']:
                        continue
                    i = s.index(w)
                    key = s[i-1] + '_' + s[i-2]
                    if w in pro_dict:
                        if key in pro_dict[w]:
                            pro_dict[w][key] += 1
                        else:
                            pro_dict[w].update({key: 1})
                    else:
                        pro_dict[w] = {key: 1}
            pro_dict_file = open(pro_dict_file_name, 'w')
            cPickle.dump(pro_dict, pro_dict_file)
        pro_dict_file.close()
        return pro_dict

    def _get_prefix_dict(self):
        prefix_dict = {}
        for d in self.pro_dict.values():
            for k, v in d.items():
                prefix_dict[k] = prefix_dict.get(k, 0) + v
        #for k in prefix_dict:
        #    print k, prefix_dict[k]
        #print len(prefix_dict)
        return prefix_dict

        


if __name__ == '__main__':
    d = ProDict('train_seg.txt')
    print u'训练集中最长词语长度：', d.longest_length
    import sys
    args = len(sys.argv)
    if 2 < args < 5:
        cur = unicode(sys.argv[1], 'utf-8')
        pre1 = unicode(sys.argv[2], 'utf-8')
        if args == 3:
            pre2 = None
        else:
            pre2 = unicode(sys.argv[3], 'utf-8')
        print cur, pre1, pre2
        if not d.has_vocable(cur):
            print u'%s 不在训练集中'% cur
        elif not d.has_vocable(pre1):
            print u'%s 不在训练集中'% pre1 
        elif (pre2 is not None) and (not d.has_vocable(pre2)):
            print u'%s 不在训练集中'% pre2
        else:
            print 'Pro is: ', d.get_pro(cur, pre1, pre2)
    else:
        print u'输入三个参数，分别为当前词，前面的词1和前面的词2'
