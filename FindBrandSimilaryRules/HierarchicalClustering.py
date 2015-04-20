#encoding=utf-8
'''
Created on Apr 15, 2015

@author: root
'''
from __future__ import division
from Utils.Cluster import *
from Utils.WordsDistance import *
from compiler.ast import List, Dict
class HierarchicalClustering():
    '''
    item : {word1,word2,dis}
    1.cal every pair words' distance
    2.the most similary pair words will be one cluster,but if there are two pair words like
    this:{(a,b)(a,d)} and if (a,d) distance >= mean_value(a,b)-some_value ,I have to add
    the pair words(a,d) to the cluster(a,b)(mean_value(a,b)=dis(a,b))
    '''
    dic={}
    threshold=1
    threshold_sort=0
    create_cluster_throd=2
    create_easy_cluster_throd=3
    vector_size=0#top n word to cal dis
    clusters=[]#cluster's list
    every_pair_words_dis_dic={}#worda@@wordb:value
    sort_dic_clusters=[]
    
    
    def __init__(self,vector_size=50,variance=0.9,mean_value=10):
        self.vector_size = vector_size
        self.variance = variance
        self.mean_value = mean_value
    def set_dic(self,dic):
        self.dic = dic
    def sort_word_dic(self,word):
        word_dic=self.dic.get(word)
        return sorted(word_dic.items(),key=lambda a:a[1].count,reverse=True)
    def get_top_word(self,sorted_dic_itemsa,sorted_dic_itemsb):
        '''
        cal how many words are the same to be two words distance
        :param sorted_dic_itemsa:
        :param sorted_dic_itemsb:
        '''
        seta=self.get_top_N_word(sorted_dic_itemsa)

        setb=self.get_top_N_word(sorted_dic_itemsb)

        return len(seta & setb)
    def get_top_N_word(self,sorted_dic_items):
        '''
        get the top n(vector_size) words to cal two words dis
        :param sorted_dic_items:
        '''
        listdata = [item[0] for item in sorted_dic_items ][:self.vector_size]
#         for item in sorted_dic_items:
#             print item[0]
        return set(listdata)
    def cal_two_word_dis(self,worda,wordb):
        '''
        cal two words dis for init the self.every_pair_words_dis_dic    
        :param worda:
        :param wordb:
        '''
        a = self.sort_word_dic(worda)
        b = self.sort_word_dic(wordb)
        return self.get_top_word(a, b)
        

    
    def union_two_cluster_words(self,one_cluster,second_cluster):
        '''
        add second_cluster's words to one_cluster's word_set
        :param one_cluster:
        :param second_cluster:
        '''
        words_set = one_cluster.word_set
        for word in second_cluster.word_set:
            words_set.add(word)
        
               
    def cal_two_cluster_mean_value(self,one_cluster,second_cluster):
        '''
        use the max distance to be two words' distance and the add the to 
        the total_value ,return the mean_value
        '''
#         print 'in cal_two_cluster_mean_value'
        total_value=0
        pair_count=0
        for o_c_word in one_cluster.word_set:
#             print 'o_c_word',o_c_word
#             print 'second_cluster.word_set ',len(second_cluster.word_set)
            max=0
            for s_c_word in second_cluster.word_set:
#                 print 's_c_word',s_c_word
#                 print o_c_word,s_c_word
                tem_dis = self.get_two_word_dis(o_c_word,s_c_word)
                if max < tem_dis:
                    max = tem_dis
#             print 'max',max
            pair_count+=1
            total_value += max
#         print self.get_two_word_dis('中午','11')
#         if total_value!=0:
#             print 'total value:',total_value
#         print pair_count
        return total_value/pair_count

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
#         for item in self.every_pair_words_dis_dic.keys():
#             print item, self.every_pair_words_dis_dic.get(item)
        print 'cal_every_pair_words_distance'
    def init_words_to_cluster(self):
        '''
        init every words to a cluster 
        '''
        for word in self.dic.keys():
            c = Cluster()
            c.word_set.add(word)
            self.clusters.append(c)
#             print 'len(c.word_set)',len(c.word_set)
        print 'init_words_to_cluster'
    def cluste(self):
        '''
        cluste the data to generate one  hierarchical
        '''
        
        new_clusters=[]
        c_id=-1
        tmp_id=-1
#         print 'clusters len: ',len(self.clusters)
        for cluster in self.clusters:
            c_id+=1
            tmp_id = -1
            tmp_cluster=self.clusters[0]
            max_dis=0
            for cluster2 in self.clusters:
                tmp_id+=1
                if cluster==cluster2:
#                     print 'cluster==cluster2'
                    continue
                tmp_dis =  self.cal_two_cluster_mean_value(cluster,cluster2)
#                 print 'tmp_dis',tmp_dis
                if max_dis<tmp_dis:
                    max_dis=tmp_dis
                    tmp_cluster = cluster2
#             print 'max_dis',max_dis
            self.tmp_cluster_or_cluster_in_exsit_cluster(new_clusters,\
                                                cluster,c_id,tmp_cluster,tmp_id,max_dis)
#             print 'process one cluster'
        self.clusters=new_clusters
        print 'len(self.clusters)',len(self.clusters)
    def tmp_cluster_or_cluster_in_exsit_cluster(self,new_clusters,\
                                                cluster,c_id,tmp_cluster,tmp_id,max_dis):
        '''
        add cluster to the clusters
        :param new_clusters:
        :param c_id:
        :param tmp_cluster:
        :param tmp_id:
        :param max_dis:
        '''
#         print 'tmp_cluster_or_cluster_in_exsit_cluster'
        a_in=False
        b_in=False
        for clu in new_clusters:
            if c_id in clu.tmp_id_list:
                a_in=True
            if tmp_id in clu.tmp_id_list:
                b_in = True
        if a_in and b_in:
            return
        if a_in:
            if max_dis>=self.cal_two_cluster_mean_value(clu,tmp_cluster)-self.threshold:
                self.add_to_exist_cluster(clu,tmp_cluster,tmp_id)
                return
        if b_in:
            if max_dis>=self.cal_two_cluster_mean_value(clu,cluster)-self.threshold:
                self.add_to_exist_cluster(clu,cluster,c_id)
                return
            print 'max_dis',max_dis
        if max_dis>self.create_cluster_throd:
            self.create_new_cluster(new_clusters,\
                                cluster,c_id,tmp_cluster,tmp_id)
        
    def create_new_cluster(self,new_clusters,\
                                cluster,c_id,tmp_cluster,tmp_id):
        '''
        create new cluster and add it to the new_clsuters
        :param new_clusters:new clusters
        :param cluster one of cluster ready to add
        :param c_id:one of cluster dynamic id
        :param tmp_cluster:
        :param tmp_id:one of cluster dynamic id
        '''
        new_cluster = Cluster()
        for words in cluster.word_set:
            new_cluster.word_set.add(words)
        for words in tmp_cluster.word_set:
            new_cluster.word_set.add(words)
        new_cluster.tmp_id_list.append(tmp_id)
        new_cluster.tmp_id_list.append(c_id)
        new_clusters.append(new_cluster)
        print 'create new cluster'
    def add_to_exist_cluster(self,clu,tmp_cluster,tmp_id):
        '''
        add cluster to exist cluster
        :param clu:the exist cluster
        :param tmp_cluster:the cluster ready to add
        :param tmp_id:cluster dynamic id
        '''
        for word in tmp_cluster.word_set:
            clu.word_set.add(word)
        clu.tmp_id_list.append(tmp_id)
        

    def run_hierarchical_clustering(self,dic):
        self.set_dic(dic)
        self.cal_every_pair_words_distance()
        self.init_words_to_cluster()
        
        for i in range(1):
            self.cluste()
        self.print_cluster()
        
    def print_cluster(self):
        of = open('../MyData/cluster_result','w')
        for clu in self.clusters:
            for word in clu.word_set:
                print >>of,word
            print>>of
            print>>of
        of.close()   
        
        
        
        
    '''
    the program below is easy cluster one pass
    '''   
    def cal_throd(self,sorted_dic):
        '''
        ?????
        '''
        leng=len(sorted_dic)
        index = int(round(leng/4))
        print 'index',index
        self.threshold_sort=1
        self.create_cluster_throd=sorted_dic[index][1]
        print 'self.create_cluster_throd',self.create_cluster_throd
    def sort_every_pair_words_dis_dic(self):
        return sorted(self.every_pair_words_dis_dic.items(),key=lambda a:a[1],reverse=True)
    def init_first_cluster(self,first_item):
        worda,wordb=self.splitword(first_item)
        self.create_sort_dic_cluster(worda, wordb, first_item[1])
    def cluste_sort_every_pair_words_dis_dic(self):
        sorted_dic = self.sort_every_pair_words_dis_dic()
        self.cal_throd(sorted_dic)
        of= open('../MyData/easy_debug','w')
        self.init_first_cluster(sorted_dic[0])
        for item in sorted_dic[1:]:
            print>>of,item[0],item[1]
            self.add_or_create_new_cluster(item)
        of.close()
    def add_or_create_new_cluster(self,sort_dic_item):
        worda,wordb = self.splitword(sort_dic_item)
        if worda == None:return
        for cluster in self.sort_dic_clusters:
            s=cluster.word_set
            if worda in s and wordb in s:
                continue
            elif worda in s :
                self.add_word_to_cluster(wordb,cluster,sort_dic_item[1])
                return
            elif wordb in s :
                self.add_word_to_cluster(worda,cluster,sort_dic_item[1])
                return
        if sort_dic_item[1]>=self.create_easy_cluster_throd:
            self.create_sort_dic_cluster(worda,wordb,sort_dic_item[1])
    def add_word_to_cluster(self,word,cluster,new_dis):
        if  new_dis>=cluster.mean_value-self.threshold_sort:
            cluster.mean_value=cluster.relation_count*cluster.mean_value+new_dis
            cluster.relation_count+=1
            cluster.mean_value/=cluster.relation_count
            cluster.word_set.add(word)
            cluster.tmp_wordsDis_list.append(new_dis)
#             print 'add',cluster.mean_value
    def create_sort_dic_cluster(self,worda,wordb,new_dis):
        cluster=Cluster()
        cluster.relation_count=1
        cluster.word_set.add(worda)
        cluster.word_set.add(wordb)
        cluster.mean_value=new_dis
        cluster.tmp_wordsDis_list.append(new_dis)
        self.sort_dic_clusters.append(cluster)
#         print 'create'
    def splitword(self,sort_dic_item):
        words = sort_dic_item[0].split('@@')
        if words[1]!=None:
            return words[0],words[1]
        return None,None
    def print_easy_cluster_result(self):
        print 'cluster len',len(self.sort_dic_clusters)
        of=open('../MyData/easy_cluster_result','w')
        for cluster in self.sort_dic_clusters:
            for word in cluster.word_set:
                print >> of,word,
            for dis in cluster.tmp_wordsDis_list:
                print>>of,dis,
            print>>of
            print >>of,cluster.mean_value
        of.close()
        
    def run_easy_clustering(self,dic):
        self.set_dic(dic)
        self.cal_every_pair_words_distance()
        self.cluste_sort_every_pair_words_dis_dic()
        self.print_easy_cluster_result()
        
        
if __name__ == '__main__':
   hc = HierarchicalClustering()
   hc.run_hierarchical_clustering(None)