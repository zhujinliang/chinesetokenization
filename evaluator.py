#! /usr/bin/python
# -*- coding: utf-8 -*-


class Evaluator(object):
    def __init__(self, result_path, test_path):
        self.result_token_list = self.get_sentence_list(result_path)
        self.test_token_list = self.get_sentence_list(test_path)
        self.total_match_num = self.get_total_match_num_of_list(self.result_token_list, self.test_token_list)

    def get_sentence_list(self, path):
        f = open(path)
        token_list = []
        for r in f:
            r = unicode(r, 'utf-8')
            tokens = r.split('  ')
            token_list.append(tokens)
        f.close()
        return token_list

    def get_match_number_of_sentence(self, result, test):
        match_num = 0
        result_length = len(result)
        test_set_length = len(test)
        i = 0
        j = 0
        while True:
            if i >= test_set_length or j >= result_length:
                break
            if i == 0:
                result_pre_length = 0
            else:
                result_pre_length = sum([len(result[n]) for n in xrange(i)])
            if j == 0:
                test_pre_length = 0
            else:
                test_pre_length = sum([len(test[n]) for n in xrange(j)])
            # To keep the pre word length is the same.
            if result_pre_length > test_pre_length:
                j += 1
            elif result_pre_length < test_pre_length:
                i += 1
            else:
                r_word_length = len(result[i])
                t_word_length = len(test[j])
                if result[i] == test[j]:
                    match_num += 1
                i += 1
                j += 1
        return match_num

    def get_total_match_num_of_list(self, result_list, test_list):
        total = 0
        result_sentences_num = len(self.result_token_list)
        test_sentences_num = len(self.test_token_list)
        if result_sentences_num != test_sentences_num:
            print 'The sentences number is not the same.'
            return total
        for i in xrange(result_sentences_num):
            total += self.get_match_number_of_sentence(self.result_token_list[i], self.test_token_list[i])
        return total


    def get_recall_rate(self):
        rate = float(self.total_match_num) / float(sum([len(w) for w in self.test_token_list]))
        return  rate

    def get_precision_rate(self):
        rate = float(self.total_match_num) / float(sum([len(w) for w in self.result_token_list]))
        return rate

if __name__ == "__main__":
    eva = Evaluator('result.txt', 'out_test_set.txt')
    print 'Precision Rate: ', eva.get_precision_rate()
    print 'Recall Rate: ', eva.get_recall_rate()
