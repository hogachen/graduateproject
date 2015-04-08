#encoding:utf-8
'''
Created on Apr 8, 2015

@author: root
'''
from WordAndTag import *
class clusterandtag():
    
    def __init__(self,cluster,tag):
        self.cluster=cluster
        self.tag=tag 
        
class SimilaryWordCluster():
    dic ={}
    def __init__(self):
        pass
    
    def read_cluster_words(self,cluster_words):
        c_w = open(cluster_words)
        tmp_cluster = ''
        for line in c_w:
            line = line.strip()
            if line == '':
                continue
            if line.find("#")>=0 and self.dic.get(line)!=None:
                tmp_cluster = line
            else:
                linesplit= line.split("@")
                if linesplit[1]=='n':
                    cat=clusterandtag(tmp_cluster,'n')
                    self.dic[line]=cat
                else:
                    tcat=clusterandtag(tmp_cluster,'a')
                    self.dic[line]=cat
    def cal_sentence_cluster(self,analysed_item,cluster_set):
        '''
        input:
        seg_sen:item[0]:tag item[1]:word
        match_items:[[('word','tag'),('word','tag')...],[('word','tag'),('word','tag')...]...]
        '''
        
        for item in analysed_item.one_short_sentence:
            cluster = self.get_word_cluster(self,item.linkword,item.linktag)
            if cluster !=None:
                if analysed_item.score>0:
                    cluster=cluster.split("#")[1].split("%")[0]
                elif analysed_item.score<0:
                    cluster=cluster.split("#")[1].split("%")[1]
                cluster_set.add(cluster)
    def get_word_cluster(self,word,tag):
        if word=='':return None
        for item in self.dic.keys():
            if word.find(item)>=0 and self.dic.get(item).tag == tag:
                return self.dic.get(item).cluster   
        
        
        
        
        
        
        
        
        
        
        