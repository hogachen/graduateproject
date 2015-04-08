#encodin=utf-8
'''
Created on Apr 6, 2015

@author: root
'''
from read_data import *
import datetime
class CalWordSimilary():
    dic={}
    def __init__(self,dic):
        self.dic = dic
    
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
                print>>outfile, v[0]+"#"+str(v[1]),
            print >>outfile
            
            
    def cal_words_similary(self):
        
        g_d_c = get_phone_collection("good_detail")
        gs_c = get_phone_collection("goods_comment")
        p_l_l=phone_logo_list()
        for logo in p_l_l:
            comment_data = get_one_logo_comment(logo,g_d_c,gs_c)
            dic_len = get_words_set(self.dic,comment_data)
            if dic_len > FINAL_DIC_SIZE:
                break    
        print 'dic length: ',dic_len
    def sortedDictValues(self,dic): 
        return sorted(dic.items(), key=lambda a: a[1],reverse=True)   
if __name__ == "__main__":
    starttime = datetime.datetime.now()
    init_ICTCLS()
    dic ={}
    cs = CalWordSimilary(dic)
    cs.cal_words_similary()
    cs.print_dic_file('../MyData/similary_dic')
    
    endtime = datetime.datetime.now()
    print "time used: %s second" %(endtime - starttime).seconds 