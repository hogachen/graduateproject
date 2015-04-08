#encoding=utf-8
'''
Created on Apr 9, 2015

@author: root
'''
from Main import *
from SimilaryWordCluster import *
class GoodItem():
    cluster_set=None
    
    def __init__(self,original_sentence,seg_sen,analysed_comment_list):
        self.original_sentence=original_sentence
        self.seg_sen=seg_sen
        self.analysed_comment_list=analysed_comment_list
        
        
class CalCluster():
    def __init__(self):
        pass
    def change_goodresult(self,goodresult):
        good_item=[]
        i=0
        short_sentence = []
        original_sentence=''
        seg_sen =None
        for item in goodresult:
            if  isinstance(item,str):
                if original_sentence != '':
                    gi = GoodItem(original_sentence,seg_sen,short_sentence)
                    good_item.append(gi)
                    original_sentence=''
                    short_sentence=[]
                i+=1
                if i==1:
                    original_sentence = item
                if i == 2:
                    seg_sen=item
                    i=0
                    continue
            short_sentence.append(item)
        return good_item
    
    
    
    
    def cal_cluster(self,goodresult,cluster_words):
        
        '''
        gooditem:
        [  ([original_sentence]   [link_tag_and_words]  
        ([[(word,tag),(word,tag)...],score],[[(word,tag),(word,tag)...],score]))...[cluster_set]]
        '''
        swc = SimilaryWordCluster()
        swc.read_cluster_words(cluster_words)
        for item in goodresult:
            if isinstance(item,str):
                continue

        gooditem = self.change_goodresult(goodresult)
        
        for item in gooditem:
            cluster_set=[]
            for item in item.analysed_comment_list:
                swc.cal_sentence_cluster(item, cluster_set)
            item.cluster_set=cluster_set
            
            
    def print_gooditem(self,good_item,filename):
        of = open(filename,'w')
        for item in good_item:
            print>>of,item.original_sentence
            print >>of,item.seg_sen
            for it in item.cluster_set:
                print >>of,it,' '
            print >>of
        
    def run(self,goodresult,cluster_words_file,outfile):
        self.cal_cluster(goodresult, cluster_words_file)
        self.print_gooditem(goodresult, outfile)



