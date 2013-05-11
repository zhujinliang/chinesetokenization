__author__ = 'zdj'
#!/usr/bin/python
# -*- coding: utf-8 -*-
class Node:

    def __init__(self,c_token,pre_token):
        self.pre_nodes=[]
        self.next_nodes=[]
        self.best_pre_node=None
        self.max_probability=0
        self.current_token=c_token
        self.pre_token=pre_token
        self.hasPass=False

    def add_pre_node(self,node):
        self.pre_nodes.append(node)

    def add_next_node(self,node):
        self.next_nodes.append(node)

    def set_best_pre_node_end_node(self,pro_dic,pre_node):
        c_token=self.current_token
        pre_1_token=pre_node.current_token
        pre_2_token=pre_node.pre_token
        translate_probability=pro_dic.get_pro(c_token,pre_1_token,pre_2_token)
        tmp_pro=translate_probability*pre_node.max_probability
        if tmp_pro>self.max_probability:
            self.max_probability=tmp_pro
            self.best_pre_node=pre_node
        self.pre_nodes.remove(pre_node)

        for node in self.pre_nodes:
            if not node.hasPass:
                return
            pre_1_token=node.current_token
            pre_2_token=node.pre_token
            translate_probability=pro_dic.get_pro(c_token,pre_1_token,pre_2_token)
            tmp_pro=translate_probability*node.max_probability
            if tmp_pro>self.max_probability:
                self.max_probability=tmp_pro
                self.best_pre_node=node
        self.hasPass=True

    def set_best_pre_node(self,pro_dic,pre_node):
        if self.current_token is 'e':
            self.set_best_pre_node_end_node(pro_dic,pre_node)
        else:
            c_token=self.current_token
            pre_1_token=self.pre_token
            pre_2_token=pre_node.pre_token
            translate_probability=pro_dic.get_pro(c_token,pre_1_token,pre_2_token)
            tmp_pro=translate_probability*pre_node.max_probability
            if tmp_pro>self.max_probability:
                self.max_probability=tmp_pro
                self.best_pre_node=pre_node
            self.pre_nodes.remove(pre_node)

            for node in self.pre_nodes:
                if not node.hasPass:
                    return
                pre_2_token=node.pre_token
                translate_probability=pro_dic.get_pro(c_token,pre_1_token,pre_2_token)
                tmp_pro=translate_probability*node.max_probability
                if tmp_pro>self.max_probability:
                    self.max_probability=tmp_pro
                    self.best_pre_node=node
            self.hasPass=True