#encoding=utf-8
'''
Created on Apr 20, 2015

@author: root
'''
from __future__ import division 
from DBOperation.DBOperation import *
class ClusterCount():
    def __init__(self,trend,count):
        self.trend = trend
        self.count = count
        
class CalGoodBadPercent():
    def __init__(self):
        pass
    
    def read_clusters(self):
        cluster_good_bad={}
        of = open('../MyData/similary_word_n')
        for line in of:
            if line.find('#')>=0:
                cluster=line.split('#')
                good=cluster[1].split('%')[0]
                bad = cluster[1].split('%')[1]
                count_list=[]
                count_list.append(ClusterCount(good,0))
                count_list.append(ClusterCount(bad,0))
                cluster_good_bad[cluster[0]]=count_list
#         for item in cluster_good_bad.items():
#             print item[1][0].trend
#             print item[0]
        of.close()
        return cluster_good_bad
    
    def cal_cluster_comment_percent(self):
        '''
        get the item_id and cal every item_id all cluster good/total percent
        '''
        best_score_except_total=0
        cluster_connection = get_collection('clusters')
        good_collection = get_collection('good_detail')
        comment_collection=get_collection('goods_comment')
        all_item_id = get_all_good_item_id(good_collection)
        icount=0
        for item_id in all_item_id:
            print 'item_id', item_id
#             if icount==1:break
#             icount+=1
            cgd= self.read_clusters()
            one_item_cluster = get_one_item_id_comment_clusters(cluster_connection,item_id)
            comm_count = get_one_good_item_comment_count(comment_collection,item_id)
            for one_cluster in one_item_cluster.items():
                for key in cgd.keys():
                    if one_cluster[0].find(key)>=0:
                        if one_cluster[0].find(cgd.get(key)[0].trend)>=0:
                            cgd.get(key)[0].count=cgd.get(key)[0].count+one_cluster[1]
                        if one_cluster[0].find(cgd.get(key)[1].trend)>=0:
                            cgd.get(key)[1].count=cgd.get(key)[1].count+one_cluster[1]
            
            for item in cgd.items():
#                 item[1].append(item[1][1].count/item[1][0].count)
                good_count=item[1][0].count
                bad_count=item[1][1].count
                if comm_count!=0:
                    good_score = round((good_count/comm_count)*500)
                    bad_score = round((bad_count/comm_count)*500)
                    total_score=50-bad_score+good_score
                else:
                    total_score=50
                if total_score>best_score_except_total and item[0]!='整体':
                    best_score_except_total=total_score
                item[1].append(total_score)
#                 print 'total_score',total_score,'comm_count',comm_count,\
#                 'good_score',good_score,\
#                 'bad_score',bad_score
                    
            add_cluster_percent_to_db(cgd,item_id,good_collection)  
        print 'best_score_except_total',best_score_except_total #550
if __name__=='__main__':
    cgbp=CalGoodBadPercent()
    cgbp.cal_cluster_comment_percent()