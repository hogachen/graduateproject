#encoding=utf-8
'''
Created on Apr 11, 2015

@author: root
'''
from CalWordSimilary.ProcessOneGood import *
from ICTCLAS_Python.nlpir import *
from DBOperation.DBOperation import *
from read_words_lib.ReadGradeWords import *

class ProcessDbData():
    def __init__(self):
        p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w = init_file()
        self.p_c_w=p_c_w
        self.n_c_w=n_c_w
        self.p_e_w=p_e_w
        self.n_e_w=n_e_w
        self.g_w_c=g_w_c
        self.n_w=n_w
        self.swc=init_swc()
        cluster_dic ={}
        readuserdic()
        SetPOSmap(2)
        self.db=get_jd_db()
        self.good_collection=get_collection('good_detail')
        self.comment_collection =get_collection('goods_comment')
        
    def create_cluster_collection(self):
        self.clusters_colleciton = create_collection('clusters')
        self.analysed_comment_collection = create_collection('analysed_comment')
    def get_last_good_item(self,setdata,list):
        newlist=[]
        for item in list:
            if item  not in setdata:
                newlist.append(item)
        return newlist
    def save_last_item(self,gid_item):
        of = open("../MyData/hadrun_good_id",'a')
        print>>of,gid_item
        of.close()
        lastitem = open('../MyData/last_item','w')
        print>>lastitem,gid_item
        lastitem.close()
    def read_ran_good_id(self):
        setdata=[]
        of = open('../MyData/hadrun_good_id')
        for item in of :
            setdata.append(item.strip())
        of.close()
        
        return setdata[:len(setdata)-1]
    def process_all_item_id_comments(self):
        firsttime=0
        setdata=self.read_ran_good_id()
        good_item_id_list_tmp = get_all_good_item_id(self.good_collection)
        good_item_id_list=self.get_last_good_item(setdata, good_item_id_list_tmp)

        for gid_item in good_item_id_list:
            
            self.save_last_item(gid_item)
            one_good_all_comment = get_one_good_all_comment(self.comment_collection,gid_item)
            
            match_goods_att(self.analysed_comment_collection,self.clusters_colleciton,\
                gid_item,one_good_all_comment,self.p_c_w,self.n_c_w,self.p_e_w,\
                self.n_e_w,self.g_w_c,self.n_w,self.swc,firsttime)
            firsttime+=1
    
    def run(self):
        self.create_cluster_collection()
        self.process_all_item_id_comments()     
if __name__=='__main__':
    pdd = ProcessDbData()    
    pdd.run()
    