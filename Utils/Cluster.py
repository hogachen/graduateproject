#encoding=utf-8
'''
Created on Apr 16, 2015

@author: root
'''
class Cluster():
    word_set=None
    mean_value=0#junzhi
    tmp_wordsDis_list=None#temp list of WordsDistance just for test
    tmp_id_list=None#id generate during the for loop so I call it tmp_id
    def __init__(self):
        self.word_set=set()
        self.tmp_id_list=[]
        self.tmp_wordsDis_list=[]
        self.relation_count=0
        self.count=0