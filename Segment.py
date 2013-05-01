__author__ = 'zdj'
import Node.py
class Segment:
    def __init__(self):
       pass
    node_list={}     #The nodes has been segment
    sentences=[]     #shor sentences
    current_index=0
    temp_node_list=[]
    pro_dictionary=None

    def in_remove_set(self,strs):
        remove_set=[u'，',u'。',u'‘',u'“',u'！',u'？',u'《',u'》',u'……',u'”',u'’',u'：',u';',u'、']
        if strs in remove_set:
            return True
        return False

    def cut_to_short_sentence(self,input_stc):
        num=len(input_stc)
        start=0
        for i in range(0,num,1):
            if self.in_remove_set(self,input_stc[i]):
                short_sentence = input_stc[start:i]
                start=i+1
                self.sentances.append(short_sentence)

    def construct_token_graph(self,short_sentence):
        num=len(short_sentence)
        num+=1
        self.temp_node_list=[]
        for i in range(0,num,1):
            node=Node()
            self.temp_node_list.append(node,None,None)
        i=j=0
        while i<num-1:

            word=short_sentence[i:j]
            if self.pro_dictionary.haskey(word):
                #  word is in the dictionary create the node, and add the connected
                node=Node(word,Node)
                self.temp_node_list[i].add_next_node(node)
                node.add_pre_node(self.temp_node_list[i])
                self.temp_node_list[j+1].add_pre_node(node)
                node.add_next_node(self.temp_node_list[j+1])
                j+=1
            else:
                if j==num-2:
                    i+=1
                    j=i
                else:
                    j+=1

        root=self.temp_node_list[0]
        root.current_token='s'
        end=self.temp_node_list[num-1]
        for i in range(1,num-2,1):
            current_node=self.temp_node_list[i]
            self.connect_token_node(current_node)
        return root, end

    def connect_token_node(self,current_node):
        n=len(current_node.next_nodes)
        new_next_nodes=[]
        for pre_node in current_node.pre_nodes:
            pre_node.next_nodes=current_node.next_nodes[:]
        for next_node in current_node.next_nodes:
            next_node.pre_nodes=current_node.pre_nodes[:]

    def is_pre_node(self,node,pre_node):
        if pre_node.current_token==node.pre_token:
            return True
        return False

    def construct_tree_lan_modle_token_graph(self,node):
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
            child_node.set_best_pre_node(self.pro_dictionary)
            self.find_max_path(child_node)

