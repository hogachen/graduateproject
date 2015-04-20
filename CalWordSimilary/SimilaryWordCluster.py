#encoding:utf-8
'''
Created on Apr 8, 2015

@author: root
'''
from Utils.WordAndTag import *
from Utils.ClusterAndTag import *
        
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
#             print line.find("%")
            if line.find("#")>=0:
                tmp_cluster = line
                continue
            else:
                linesplit= line.split("@")
#                 print line
                if linesplit[1]=='n':
                    cat=ClusterAndTag(tmp_cluster,'n')
                    self.dic[linesplit[0]]=cat
                else:
                    cat=ClusterAndTag(tmp_cluster,'a')
                    self.dic[linesplit[0]]=cat
    def cal_sentence_cluster(self,analysed_item):
        '''
        input:
        seg_sen:item[0]:tag item[1]:word
        match_items:[[('word','tag'),('word','tag')...],[('word','tag'),('word','tag')...]...]
        '''
        
        for item in analysed_item.one_short_sentence:
            cluster = self.get_word_cluster(item.linkword,item.linktag)
            if cluster !=None:
                if analysed_item.score != 0:
                    head,good,bad=self.cut_cluter_title(cluster)
                if analysed_item.score>0:
                    cluster=head+good
                elif analysed_item.score<0:
                    cluster=head+bad
#                 print cluster
                return cluster
#                 cluster_set.append(cluster)
                
                
                
    def cut_cluter_title(self,cluster):
        '''
        just for not split too many times
        '''
        tmpcut = cluster.split("#")
        head = tmpcut[0]
        tmpcut_tend=tmpcut[1].split("%")
        good = tmpcut_tend[0]
        bad = tmpcut_tend[1]
        return head,good,bad
    def get_word_cluster(self,word,tag):
        if word=='':return None
        for item in self.dic.keys():
#             print item
            if word.find(item)>=0 and self.dic.get(item).tag == tag:
#                 print self.dic.get(item).cluster
                return self.dic.get(item).cluster   
        return None
        
        
        
        
        
        
        
        
        
        