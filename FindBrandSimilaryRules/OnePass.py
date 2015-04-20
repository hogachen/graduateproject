#encoding=utf-8
'''
Created on Apr 19, 2015

@author: root
'''
import math
from __future__ import division
from Utils.Cluster import *
from ClusterTools import *
class OnePass():
    throd=0
    def __init__(self,dic):
        self.dic = dic
        self.clusters=[]
        self.every_pair_words_dis_dic={}
    def init_first_cluster(self,word):
        cluster=Cluster()
        cluster.word_set.add(word)
        
    def cal_every_pair_words_distance(self):
        '''
        init the self.every_pair_words_dis_dic
        '''
        if self.dic=={}:
            self.every_pair_words_dis_dic=None
            return
        keys=self.dic.keys()
        key_count=0;
        for key in keys[:len(keys)-1]:
            key_count+=1
            for sec_key in keys[key_count:]:
                dis = self.cal_two_word_dis(key,sec_key)
                if dis != 0:
                    self.every_pair_words_dis_dic[key+'@@'+sec_key]=dis
        print 'cal_every_pair_words_distance'


    def cal_two_word_dis(self,worda,wordb):
        '''
        cal two words dis for init the self.every_pair_words_dis_dic    
        :param worda:
        :param wordb:
        '''
        a = self.sort_word_dic(worda)
        b = self.sort_word_dic(wordb)
        return self.get_top_word(a, b)
    
    def get_top_word(self,sorted_dic_itemsa,sorted_dic_itemsb):
        '''
        cal how many words are the same to be two words distance
        :param sorted_dic_itemsa:
        :param sorted_dic_itemsb:
        '''
        seta=self.get_top_N_word(sorted_dic_itemsa)

        setb=self.get_top_N_word(sorted_dic_itemsb)

        return len(seta & setb)
    
    def sort_word_dic(self,word):
        word_dic=self.dic.get(word)
        return sorted(word_dic.items(),key=lambda a:a[1].count,reverse=True)
    
    
    def get_two_word_dis(self,o_c_word,s_c_word):
        '''
        when cal two cluster'dis(also mean_value),I cal every pairs word'd 
        distance beforehand and restore them in the self.two_words_dis_dic
        with the form like {'worda@@wordb':value}
        :param o_c_word:
        :param s_c_word:
        '''
        dis = self.every_pair_words_dis_dic.get(o_c_word+'@@'+s_c_word)
        dis2 = self.every_pair_words_dis_dic.get(s_c_word+'@@'+o_c_word)
#         print dis,self.every_pair_words_dis_dic.get(self.every_pair_words_dis_dic.keys()[0])
        if dis != None:
            return dis
        if dis2 != None:
            return dis2
        return 0


    def add_word_to_most_similary_cluster(self,word):
        max_dis=0
        tmp_cluster=self.clusters[0]
        for clu_item in self.clusters[1:]:
            tmp_dis=self.cal_word_cluster_distance(word,clu_item)
            if tmp_dis>max_dis:
                max_dis=tmp_dis
                tmp_cluster=clu_item
        if max_dis>self.thord:
            self.add_word_to_set(word, tmp_cluster)
        else:
            self.create_new_cluster()
    def create_new_cluster(self,word):
        cluster = Cluster()
        cluster.word_set.add(word)
        self.clusters.append(cluster)
    def add_word_to_set(self,word,cluster):
        cluster.word_set.add(word)
    def cal_word_cluster_distance(self,word,cluster):
        '''
        it is the most important to define the dis ?????
        :param word:
        :param cluster:
        '''
        total_dis=0
        for set_word in cluster.word_set:
            total_dis+=self.get_two_word_dis(word, set_word)
        return total_dis/len(cluster.word_set)
    def cal_throd(self):
        mean_value=0
        variance =0
        count=2
        for value in self.every_pair_words_dis_dic.value():
            before_mean_value=mean_value
            mean_value=((count-1)*mean_value+value)/count
            variance=(count-2)*variance/(count-1)+(value-before_mean_value)*(value-before_mean_value)/count
            count+=1
        self.throd = mean_value+0.5*math.sqrt(variance)
    def one_pass(self,dic):
        self.dic=dic
        self.cal_throd()
        self.cal_every_pair_words_distance()
        key_list=self.dic.keys()
        self.init_first_cluster(key_list[0])
        for key in key_list[1:]:
            self.add_word_to_most_similary_cluster(key)
    def run(self):
        
                