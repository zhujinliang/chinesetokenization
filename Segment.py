#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zdj'
from Node import *
from pro_dict import *
import re
import datetime


class Segment(object):
    def __init__(self):
        self.node_list = {}       # The nodes has been segment
        self.sentences = []       # short sentences
        self.current_index = 0
        self.temp_node_list = []
        self.pro_dictionary = None
        self.graph_nodes_list = []
        self.debug = False
        self.separator = u'  '

    def cut_into_short_sentence(self, input_stc):
        re_biaodian = re.compile(ur'[\u2014-\u2026\u3000-\u303F\uff01-\uff0c\uff1a-\uff1f]')
        line = unicode(input_stc, 'utf-8')
        line = line.strip()
        self.sentences = re_biaodian.split(line)
        for sen in self.sentences:
            if sen is u'':
                self.sentences.remove(sen)

    def create_new_connected_node(self, word, pre_node, next_node):
        node = Node(word, None)

        pre_node.add_next_node(node)
        node.add_pre_node(pre_node)

        next_node.add_pre_node(node)
        node.add_next_node(next_node)
        return node

    def construct_token_graph(self, short_sentence):
        # short_sentence is not start with  's' and end with 'e'
        num = len(short_sentence)
        num += 1

        self.temp_node_list = []
        self.graph_nodes_list = []
        for i in range(0, num, 1):
            node = Node(None, None)
            self.temp_node_list.append(node)
        for i in range(0, num - 1, 1):
            word = short_sentence[i]
            node = self.create_new_connected_node(word, self.temp_node_list[i], self.temp_node_list[i + 1])
            self.graph_nodes_list.append(node)
        if num > 2:
            i = 0
            j = i + 2
        else:
            i = 0
            j = i + 1

        while i < num - 1:
            word = short_sentence[i:j]
            if self.pro_dictionary.has_vocable(word):
                if self.debug:
                    print 'In Dictionary: ' + i.__str__() + ' ' + j.__str__() + ' ' + word
                node = self.create_new_connected_node(word, self.temp_node_list[i], self.temp_node_list[j])
                self.graph_nodes_list.append(node)
                if j < num - 1:
                    j += 1
                else:
                    i += 1
                    j = i + 2
                    if j >= num - 1:
                        break
            else:
                # word is not in the dictionary go to the next word
                # j is at the end of the sentence
                if j >= num - 1 or j - i >= self.pro_dictionary.get_longest_length():
                    i += 1
                    j = i + 2
                    if j > num - 1:
                        break
                else:
                    if j < num - 1:
                        j += 1
                    else:
                        # when the i point to the last character of the sentence break
                        i += 1
                        j = i + 2
                        if j > num - 1:
                            break

        root = self.temp_node_list[0]
        root.current_token = 's'
        end = self.temp_node_list[num - 1]
        end.current_token = 'e'

        for i in range(1, num - 1, 1):
            current_node = self.temp_node_list[i]
            self.connect_token_node(current_node)
        return root, end

    def connect_token_node(self, current_node):
        for pre_node in current_node.pre_nodes:
            pre_node.next_nodes = current_node.next_nodes[:]
        if len(current_node.next_nodes) is 1 and current_node.next_nodes[0].current_token is 'e':
            end = current_node.next_nodes[0]
            end.pre_nodes.remove(current_node)
            for pre in current_node.pre_nodes:
                end.pre_nodes.append(pre)
        else:
            for next_node in current_node.next_nodes:
                next_node.pre_nodes = current_node.pre_nodes[:]

    def is_pre_node(self, node, pre_node):
        if pre_node.current_token == node.pre_token:
            return True
        return False

    def construct_three_token_graph_phase_1(self, node):
        # add a new node to replace the original edge between two nodes
        # not the end node of the graph
        if not node.current_token == 'e':
            num = len(node.next_nodes)
            for i in range(0, num, 1):
                next_node = node.next_nodes[i]
                if next_node.pre_token is not None or next_node.current_token is 'e':
                    continue
                else:
                    token = next_node.current_token
                    new_node = Node(token, node.current_token)
                    new_node.pre_nodes.append(node)
                    new_node.next_nodes.append(next_node)

                    node.next_nodes[i] = new_node

                    node_index = next_node.pre_nodes.index(node)
                    next_node.pre_nodes[node_index] = new_node

                    self.construct_three_token_graph_phase_1(next_node)
        else:
            return

    def construct_three_token_graph_phase_2(self):
        # remove the single token node
        for node in self.graph_nodes_list:
            self.connect_token_node(node)

    def construct_three_lan_model_token_graph(self, node):
        if len(node.next_nodes) == 0:
            return
        n = len(node.pre_nodes)
        if n == 1:
            node.pre_token = node.pre_nodes[0].current_token
            for next_node in node.next_nodes:
                self.construct_tree_lan_modle_token_graph(next_node)
        else:
            split_nodes = []
            for pre_node in node.pre_nodes:
                has_node = False

                for split_new_node in split_nodes:
                    if self.is_pre_node(split_new_node, pre_node):
                        pre_node.next_nodes.remove(node)
                        pre_node.next_nodes.append(split_new_node)
                        has_node = True
                        break

                if not has_node:
                    new_node = Node(node.current_token, pre_node.current_token)
                    new_node.pre_nodes.append(pre_node)
                    new_node.next_nodes = node.next_nodes[:]

                    pre_node.next_nodes.remove(node)
                    pre_node.next_nodes.append(split_new_node)

            del node
            for new_node in split_nodes:
                for next_node in new_node.next_nodes:
                    self.construct_tree_lan_modle_token_graph(next_node)

    def find_max_path(self, root):
        if len(root.next_nodes) == 0:
            return
        for child_node in root.next_nodes:
            child_node.set_best_pre_node(self.pro_dictionary, root)
            if child_node.hasPass:
                self.find_max_path(child_node)

    def final_token_path(self, node):
        if node.current_token == 'e':
            node = node.best_pre_node
            self.final_token_path(node)
        elif node.current_token == 's':
            return
        else:
            self.result_token.append(node.current_token)
            node = node.best_pre_node
            self.final_token_path(node)

    def scan_sentence_for_result(self, tokens, sentence):
        sentence = unicode(sentence, 'utf-8')
        sentence = sentence.strip()
        start_index = 0
        re_biaodian = re.compile(ur'[\u2014-\u2026\u3000-\u303F\uff01-\uff0c\uff1a-\uff1f]')
        i = 0
        while i < len(tokens):
            l = len(tokens[i])
            word = sentence[start_index:start_index + l]
            # if word == u'，':
            #     pass
            # if tokens[i] == u'如果':
            #     pass
            if not word == tokens[i]:
                if re_biaodian.match(sentence[start_index]):
                    tokens.insert(i, sentence[start_index])
                else:
                    print'Error not match character'
                start_index += 1
            else:
                start_index += l
            i += 1
        n = len(sentence)
        if start_index < n:
            word = sentence[start_index:n]
            tokens.append(word)
        return tokens

    def segment(self, sentences):
        seg_sentence = []
        for sentence in sentences:
            tokens = []
            self.cut_into_short_sentence(sentence)
            for short_sentence in self.sentences:
                start_time_1 = datetime.datetime.now()
                root, end = self.construct_token_graph(short_sentence)
                start_time_2 = datetime.datetime.now()
                self.construct_three_token_graph_phase_1(root)
                start_time_3 = datetime.datetime.now()
                self.construct_three_token_graph_phase_2()
                start_time_4 = datetime.datetime.now()
                root.max_probability = 1
                self.find_max_path(root)
                start_time_5 = datetime.datetime.now()
                self.result_token = []
                self.final_token_path(end)
                start_time_6 = datetime.datetime.now()
                self.result_token.reverse()
                tokens.__iadd__(self.result_token)
                if self.debug:
                    print 'construct_token_graph time:          ' + (start_time_2 - start_time_1).microseconds.__str__()
                    print 'construct_three_token_graph_phase_1: ' + (start_time_3 - start_time_2).microseconds.__str__()
                    print 'construct_three_token_graph_phase_2: ' + (start_time_4 - start_time_3).microseconds.__str__()
                    print 'find_max_path:                       ' + (start_time_5 - start_time_4).microseconds.__str__()
                    print 'final_token_path:                    ' + (start_time_6 - start_time_5).microseconds.__str__()
                    print u'/'.join(self.result_token)
            tokens = self.scan_sentence_for_result(tokens, sentence)
            result_str = self.separator.join(tokens)
            result_str += '\n'
            seg_sentence.append(result_str)
        return seg_sentence


if __name__ == '__main__':

    input_file = open('input_sentence.txt')
    sens = input_file.readlines()
    # print sens[0]
    # re_biaodian = re.compile(ur'[\u2014-\u2026\u3000-\u303F\uff01-\uff0c\uff1a-\uff1f]')
    # line=u'本报巴黎２月５日电记者王芳报道：第一届欧亚文化论坛今天在巴黎开幕。中国代表团团长、中国驻法国公使衔文化参赞吴春德在今天的全体会议上作了发言。他指出，亚欧两大陆间的文化交流源远流长，在当今世界格局向多极化方向发展的时代，加强亚欧文化交流和合作，是亚欧间建立新型全面伙伴关系的重要方面。开展亚欧文化合作应遵循互相尊重、平等互利、求同存异、不干涉他国内政的原则。吴春德向大会提出了４项建议：２０００年在中国等国举办《亚欧文明集粹》展；加强亚欧艺术教育方面的交流；今年在中国举办“中国国际美术年”；中国愿在欧盟的支持下，派出优秀艺术团赴欧演出和举办文物展。'
    # sens=re_biaodian.split(line)
    # for s in sens:
    #     print s
    # print sens
    seg = Segment()
    pro_dic = ProDict()
    seg.pro_dictionary = pro_dic
    results=seg.segment(sens)
    for result in results:
        print result
