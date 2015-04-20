#encodin=utf-8
'''
Created on Apr 6, 2015

@author: root
'''
from read_data import *
from DBOperation.DBOperation import *
import datetime
from HierarchicalClustering import *
class CalWordSimilary():
    dic={}
    relate_word_dic={}
    def __init__(self,dic,window_size=10,relate_window=50):
        '''
        if window_size==10 it means cal similary in mean group
        else window_size==1or2 it means cal in small windowsize
        :param dic:
        :param window_size:
        :param relate_window:
        '''
        self.dic = dic
        self.window_size=window_size
        self.relate_window = relate_window
    
    def cal_word_similiary(self,word1,word2):
        if word1.strip()=='' or word2.strip() == '':
            return None
        word1_dic = self.dic.get(word1)
        similary =  word1_dic.get(word2)
        if similary != None:
            return similary
        return None
    def print_dic_file(self,outfile_path):
        outfile = open(outfile_path,'w')
        for key in self.dic.keys():
            print >> outfile ,key
            value = self.dic.get(key)
            sort_dic = self.sortedDictValues(value)
            for v in sort_dic:
                print>>outfile, v[0]+"#"+str(v[1].count)+str(v[1].tag),
            print >>outfile
        print 'print to similary_dic'   
            
    def cal_words_similary(self):
        stop_word=read_stop_word()
        g_d_c = get_phone_collection("good_detail")
        gs_c = get_phone_collection("goods_comment")
        p_l_l=phone_logo_list()
        for logo in p_l_l:
            comment_data = get_one_logo_comment(logo,g_d_c,gs_c)
            dic_len = get_words_set(self.dic,comment_data,self.window_size,stop_word)
            if dic_len > FINAL_DIC_SIZE:
                break    
        print 'dic length: ',dic_len
        self.print_dic_file('../MyData/similary_dic')
    def sortedDictValues(self,dic): 
#         {'good':('n',12)}
        return sorted(dic.items(), key=lambda a: a[1].count,reverse=True)   
#         return sorted(dic.items(), lambda a,b: cmp(a[1][1], b[1][1]),reverse=True)  
    def find_relate_words(self):
        if self.dic !=None:
            for key in self.dic.keys():
                for item in self.dic.get(key):
#                     print item[0]
                    if self.is_key_in_sorted_list(key,self.dic.get(item[0])):
                        if self.relate_word_dic.get(key)!=None:
                            self.relate_word_dic.get(key).append(item)
                        else:
                            list = []
                            list.append(item)
                            self.relate_word_dic[key]=list
    def is_key_in_sorted_list(self,key,list):
        for list_item in list:
            if key == list_item[0]:
                return True
    def change_oridic_sorted(self):
        for key in self.dic.keys():
            dic[key]=self.get_relate_window_word(key)
    def print_relate_word_dic(self):
        of = open('../MyData/relate_words','w')
        for key in self.relate_word_dic.keys():
            print >>of,key
            list = self.relate_word_dic.get(key)
            for item in list:
                print >>of,item[0]+""+str(item[1].count)+str(item[1].tag),
            print >>of
            print >>of
        of.close()
    def get_relate_window_word(self,key):
        sortd_relate_word = self.sortedDictValues(self.dic.get(key))
        i = 0
        toplist=[]
        for item in sortd_relate_word:
            if i == self.relate_window:break
            toplist.append(item)
            i+=1
        return toplist
    def cal_relate_word(self):
        self.change_oridic_sorted()
        self.find_relate_words()
        self.print_relate_word_dic()
    def hierarchical_clustering(self):
        hc = HierarchicalClustering()
        hc.run_hierarchical_clustering(self.dic)
    def easy_clustering(self):
        hc = HierarchicalClustering()
        hc.run_easy_clustering(self.dic)
if __name__ == "__main__":
    
    starttime = datetime.datetime.now()
    init_ICTCLS()
    dic ={}
    
    
    
    cs = CalWordSimilary(dic)
    cs.cal_words_similary()
#     cs.cal_relate_word()
#     cs.hierarchical_clustering()
    cs.easy_clustering()
    
    
    
    endtime = datetime.datetime.now()
    print "time used: %s second" %(endtime - starttime).seconds 
    
    
    