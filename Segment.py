#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zdj'
from Node import *
from pro_dict import *
import re
import datetime

class Segment:
    def __init__(self):
        self.node_list={}       #The nodes has been segment
        self.sentences=[]       #shor sentences
        self.current_index=0
        self.temp_node_list=[]
        self.pro_dictionary=None
        self.graph_nodes_list=[]

    def cut_into_short_sentence(self,input_stc):
        re_biaodian = re.compile(ur'[\u2014-\u2026\u3000-\u303F\uff01-\uff0c\uff1a-\uff1f]')

        line=unicode(input_stc,'utf-8')
        line=line.strip()
        self.sentences=re_biaodian.split(line)
        for sen in self.sentences:
            if sen is u'':
                self.sentences.remove(sen)
    def create_new_connected_node(self,word,pre_node,next_node):
        node=Node(word,None)

        pre_node.add_next_node(node)
        node.add_pre_node(pre_node)

        next_node.add_pre_node(node)
        node.add_next_node(next_node)
        return node

    def construct_token_graph(self,short_sentence):
        # short_sentence is not start with  's' and end with 'e'
        num=len(short_sentence)
        num+=1

        self.temp_node_list=[]
        self.graph_nodes_list=[]
        for i in range(0,num,1):
            node=Node(None,None)
            self.temp_node_list.append(node)
        for i in range(0,num-1,1):
            word=short_sentence[i]
            node=self.create_new_connected_node(word,self.temp_node_list[i],self.temp_node_list[i+1])
            self.graph_nodes_list.append(node)
        i=0
        j=i+2

        while i<num-1:
            word=short_sentence[i:j]

            if self.pro_dictionary.has_vocable(word):
                print 'In Dictionary: '+i.__str__()+' '+j.__str__()+' '+word
                node=self.create_new_connected_node(word,self.temp_node_list[i],self.temp_node_list[j])
                self.graph_nodes_list.append(node)
                if j<num-1:
                    j+=1
                else:
                    i+=1
                    j=i+2
                    if j>=num-1:
                        break
            else:
                #word is not in the dictionary go to the next word
                if j>=num-1 or j-i>=self.pro_dictionary.get_longest_length():#j is at the end of the sentence
                    i+=1
                    j=i+2
                    if j>num-1:
                        break
                else:
                    if j<num-1:
                        j+=1
                    else:
                        # when the i point to the last character of the sentence break
                        i+=1
                        j=i+2
                        if j>num-1:
                            break

        root=self.temp_node_list[0]
        root.current_token='s'
        end=self.temp_node_list[num-1]
        end.current_token='e'

        for i in range(1,num-1,1):
            current_node=self.temp_node_list[i]
            self.connect_token_node(current_node)
        return root, end

    def connect_token_node(self,current_node):
        for pre_node in current_node.pre_nodes:
            pre_node.next_nodes=current_node.next_nodes[:]
        if len(current_node.next_nodes) is 1 and current_node.next_nodes[0].current_token is 'e':
            end=current_node.next_nodes[0]
            end.pre_nodes.remove(current_node)
            for pre in current_node.pre_nodes:
                end.pre_nodes.append(pre)
        else:
            for next_node in current_node.next_nodes:
                next_node.pre_nodes=current_node.pre_nodes[:]

    def is_pre_node(self,node,pre_node):
        if pre_node.current_token==node.pre_token:
            return True
        return False
    def construct_three_token_graph_phase_1(self,node):
        # add a new node to replace the original edge between two nodes
        # not the end node of the graph
        if not node.current_token=='e':
            num=len(node.next_nodes)
            for i in range(0,num,1):
                next_node=node.next_nodes[i]
                if next_node.pre_token!=None or next_node.current_token is 'e':
                    continue
                else:
                    token=next_node.current_token

                    new_node=Node(token,node.current_token)
                    new_node.pre_nodes.append(node)
                    new_node.next_nodes.append(next_node)

                    node.next_nodes[i]=new_node

                    node_index=next_node.pre_nodes.index(node)
                    next_node.pre_nodes[node_index]=new_node

                    self.construct_three_token_graph_phase_1(next_node)
        else:
            return

    def construct_three_token_graph_phase_2(self,node):
        #remove the single token node
        for node in self.graph_nodes_list:
            self.connect_token_node(node)

    def construct_three_lan_modle_token_graph(self,node):
        if len(node.next_nodes)==0:
            return
        n=len(node.pre_nodes)
        if n==1:
            node.pre_token=node.pre_nodes[0].current_token
            for next_node in node.next_nodes:
                self.construct_tree_lan_modle_token_graph(next_node)
        else:
            split_nodes=[]
            for pre_node in node.pre_nodes:
                has_node=False

                for split_new_node in split_nodes:
                    if self.is_pre_node(split_new_node,pre_node):
                        pre_node.next_nodes.remove(node)
                        pre_node.next_nodes.append(split_new_node)
                        has_node=True
                        break

                if not has_node:
                    new_node=Node(node.current_token,pre_node.current_token)
                    new_node.pre_nodes.append(pre_node)
                    new_node.next_nodes=node.next_nodes[:]

                    pre_node.next_nodes.remove(node)
                    pre_node.next_nodes.append(split_new_node)

            del node
            for new_node in split_nodes:
                for next_node in new_node.next_nodes:
                    self.construct_tree_lan_modle_token_graph(next_node)

    def find_max_path(self,root):
        if len(root.next_nodes)==0:
            return
        for child_node in root.next_nodes:
            child_node.set_best_pre_node(self.pro_dictionary,root)
            if child_node.hasPass:
                self.find_max_path(child_node)

    result_token=[]
    def final_token_path(self,node):
        if node.current_token=='e':
            node=node.best_pre_node
            self.final_token_path(node)
        elif node.current_token=='s':
            return
        else:
            self.result_token.append(node.current_token)
            node=node.best_pre_node
            self.final_token_path(node)
    def scane_sentence_for_result(self,tokens,sentence):
        sentence=unicode(sentence,'utf-8')
        sentence=sentence.strip()
        startindex=0
        re_biaodian = re.compile(ur'[\u2014-\u2026\u3000-\u303F\uff01-\uff0c\uff1a-\uff1f]')
        n=len(tokens)
        i=0
        while i<len(tokens):
            l=len(tokens[i])
            word=sentence[startindex:startindex+l]
            if word==u'，':
                pass
            if tokens[i]==u'如果':
                pass
            if not word==tokens[i]:
                if re_biaodian.match(sentence[startindex]):
                    tokens.insert(i,sentence[startindex])
                    n=len(tokens)
                else:
                    print'Error not match character'
                startindex+=1
            else:
                startindex+=l
            i+=1
        n=len(sentence)
        if startindex<n:
            word=sentence[startindex:n]
            tokens.append(word)


        return tokens

    def segment(self,sentences):
        seg_sentence=[]
        for sentence in sentences:
            tokens=[]
            self.cut_into_short_sentence(sentence)
            for short_sentence in self.sentences:
                stattime1=datetime.datetime.now()
                root, end=self.construct_token_graph(short_sentence)
                starttime2=datetime.datetime.now()
                self.construct_three_token_graph_phase_1(root)
                starttime3=datetime.datetime.now()
                self.construct_three_token_graph_phase_2(root)
                starttime4=datetime.datetime.now()
                root.max_probability=1
                self.find_max_path(root)
                datetime5=datetime.datetime.now()
                self.result_token=[]
                self.final_token_path(end)
                starttime6=datetime.datetime.now()
                self.result_token.reverse()
                tokens.__iadd__(self.result_token)
                print 'construct_token_graph time:          '+(starttime2 - stattime1).microseconds.__str__()
                print 'construct_three_token_graph_phase_1: '+(starttime3-starttime2).microseconds.__str__()
                print 'construct_three_token_graph_phase_2: '+(starttime4-starttime3).microseconds.__str__()
                print 'find_max_path:                       '+(datetime5-starttime4).microseconds.__str__()
                print 'final_token_path:                    '+(starttime6-datetime5).microseconds.__str__()
                print u'/'.join(self.result_token)
            tokens=self.scane_sentence_for_result(tokens,sentence)
            print  u' '.join(tokens)
            seg_sentence.append(tokens)


if __name__=='__main__':

    input_file=open('input_sentence.txt')
    sens=input_file.readlines()
    print sens[0]
    # re_biaodian = re.compile(ur'[\u2014-\u2026\u3000-\u303F\uff01-\uff0c\uff1a-\uff1f]')
    # line=u'你 好，：：再见'
    # sens=re_biaodian.split(line)
    # for s in sens:
    #     print s
    # print sens
    seg=Segment()
    pro_dic=ProDict('train_seg.txt')
    seg.pro_dictionary=pro_dic
    seg.segment(sens)