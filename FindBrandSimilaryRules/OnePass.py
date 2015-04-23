#encoding=utf-8
'''
Created on Apr 19, 2015

@author: root
'''

from __future__ import division
import math
import random
from Utils.Cluster import *
from ClusterTools import *
from Tools.easy_print import *
import dis
class OnePass():
    throd=0
    def __init__(self,dic,vector_size=50):
        self.dic = dic
        self.vector_size=vector_size
        self.clusters=[]
        self.every_pair_words_dis_dic={}
        self.create_throd=1#it must greater than this throd to be a new cluster
        self.new_throd=3#when greater than this throd i add the word to cluster
    def cal_create_throd(self):
        keylist=self.dic.keys()
        json_print(keylist)
        length = len(keylist)
        total=0
        count=0
        for i in range(int(length/2)):
            index1 = random.randrange(0,length-1, 1)
            index2 = random.randrange(0, length-1, 1)
            worda = keylist[index1]
            wordb = keylist[index2]
            dis = self.cal_two_word_dis_have_sorted(worda, wordb)
            total+=dis
            count+=1
            print worda,wordb,dis
        self.create_throd=total/count
        print 'elf.create_throd', self.create_throd,'total',total,count
    def sortedDictValues(self,dic): 
#         {'good':('n',12)}
        return sorted(dic.items(), key=lambda a: a[1].count,reverse=True)   
#         return sorted(dic.items(), lambda a,b: cmp(a[1][1], b[1][1]),reverse=True)   
    def change_oridic_sorted_for_onepass(self):
        for key in self.dic.keys():
            self.dic[key]=self.get_relate_window_word_onepass(key)
    def get_relate_window_word_onepass(self,key):
        sortd_relate_word = self.sortedDictValues(self.dic.get(key))
        i = 0
        toplist=[]
        for item in sortd_relate_word:
            if i == self.vector_size:break
            toplist.append(item[0])
            i+=1
        
        return toplist
    def init_first_cluster_easy(self,word):
        max = 0
        tmp_key=''
        for key in self.dic.keys():
            if key==word:continue
            tmp = self.cal_two_word_dis_have_sorted(word, key)
            if max<tmp:
                max=tmp
                tmp_key=key
        if  max > self.create_throd:
            cluster = self.create_new_cluster(word)
            self.add_word_to_set_easy(tmp_key, cluster,max)
#             print json_print(list(cluster.word_set)),cluster.tmp_wordsDis_list,cluster.mean_value
    def init_first_cluster(self,word):
        cluster=Cluster()
        cluster.word_set.add(word)
        self.clusters.append(cluster)
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
    def get_top_N_word(self,sorted_dic_items):
        '''
        get the top n(vector_size) words to cal two words dis
        :param sorted_dic_items:
        '''
        listdata = [item[0] for item in sorted_dic_items ][:self.vector_size]
#         for item in sorted_dic_items:
#             print item[0]
        return set(listdata)
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
        if max_dis>self.throd:
            self.add_word_to_set(word, tmp_cluster)
        else:
            self.create_new_cluster(word)
    def add_word_to_most_similary_cluster_easy(self,word):
        have_add=0
        max_clu_dis=0
        tmp_max_clu=self.clusters[0]
        for clu_item in self.clusters:
            tmp_dis=self.cal_word_cluster_distance(word,clu_item)
            if tmp_dis>=clu_item.mean_value:
                have_add=1
                self.add_word_to_set_easy(word, clu_item,tmp_dis)
        if have_add==0:
            self.init_first_cluster_easy(word)
    def add_word_to_most_similary_cluster_easy2(self,word):
        max_clu_dis=0
        tmp_max_clu=None
        for clu_item in self.clusters:
            tmp_dis=self.cal_word_cluster_distance(word,clu_item)
            if tmp_dis>max_clu_dis:
                max_clu_dis=tmp_dis
                tmp_max_clu=clu_item
        if max_clu_dis >= self.new_throd:
            self.add_word_to_set_easy(word, tmp_max_clu,max_clu_dis)
        else:
            self.init_first_cluster_easy(word)
    def add_word_to_set_easy(self,word, clu_item,dis):
        clu_item.word_set.add(word)
        clu_item.count+=1
        if clu_item.count>=2:
            before_mean_value=clu_item.mean_value
            clu_item.mean_value=((clu_item.count-1)*before_mean_value+dis)/clu_item.count
        else:
            clu_item.mean_value=dis
        clu_item.tmp_wordsDis_list.append(dis)
    def create_new_cluster(self,word):
        cluster = Cluster()
        cluster.word_set.add(word)
        self.clusters.append(cluster)
        return cluster
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
            total_dis+=self.cal_two_word_dis_have_sorted(word, set_word)
        return total_dis/len(cluster.word_set)
    def cal_two_word_dis_have_sorted(self,word, set_word):
        return len(set(self.dic.get(word))&set(self.dic.get(set_word)))
    def cal_throd(self):
        mean_value=0
        variance =0
        count=2
        for value in self.every_pair_words_dis_dic.values():
            before_mean_value=mean_value
            mean_value=((count-1)*mean_value+value)/count
            variance=(count-2)*variance/(count-1)+(value-before_mean_value)*(value-before_mean_value)/count
            count+=1
        self.throd = mean_value+0.5*math.sqrt(variance)
        self.throd=self.throd*1
        print self.throd
    def print_one_pass_result(self):
        of = open('../MyData/onepass_result','w')
        for clu in self.clusters:
            for word in clu.word_set:
                print >>of ,word,
            print >>of
            for dis in clu.tmp_wordsDis_list:
                print>>of,dis,
            print>>of
            print >>of,clu.mean_value
        of.close()
        
        
        
    def cal_word_cluster_distance_easy(self,word,cluster):
        '''
        it is the most important to define the dis ?????
        :param word:
        :param cluster:
        '''
        max_dis=0
        
        for set_word in cluster.word_set:
            if set_word==word:continue
            tmp_dis = self.cal_two_word_dis_have_sorted(word, set_word)
            if max_dis < tmp_dis:
                max_dis=tmp_dis
        return max_dis
    def one_pass(self):
#         self.cal_every_pair_words_distance()
#         self.cal_throd()
        self.change_oridic_sorted_for_onepass()
#         self.cal_create_throd()
        key_list=self.dic.keys()
        self.init_first_cluster_easy(key_list[0])
        for key in key_list[1:]:
            self.add_word_to_most_similary_cluster_easy2(key)
            self.print_one_pass_result()

        
        
                