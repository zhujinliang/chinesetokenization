__author__ = 'zdj'
class Node:
    pre_nodes=[]
    next_nodes=[]
    best_pre_node=None
    max_probability=1
    current_token=''  #token
    pre_token=None


    def __init__(self,c_token,pre_token):
        self.current_token=c_token
        self.pre_token=pre_token

    def add_pre_node(self,node):
        self.pre_nodes.append(node)

    def add_next_node(self,node):
        self.next_nodes.append(node)

    def set_best_pre_node(self,pro_dic):
        c_token=self.current_token
        pre_1_token=self.pre_token
        pre_2_token=None
        for node in self.pre_nodes:
            pre_2_token=node.pre_token
            translate_probability=pro_dic.get_probability(c_token,pre_1_token,pre_2_token)
            tmp_pro=translate_probability*node.max_probability
            if tmp_pro>self.max_probability:
                self.max_probability=tmp_pro
                self.best_pre_node=node