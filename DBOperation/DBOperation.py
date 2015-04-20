#encoding:utf-8
'''
Created on Apr 6, 2015

@author: root
'''
from Utils.Comment import *
# from Comment import *
from Tools.PreprocessSentence import *
from mongo_connection import *
from Tools.easy_print import json_print
def get_jd_db():
    mgdb = MongoConnection()
    return mgdb.getJDDB()
def phone_logo_list():
    list = "三星（SAMSUNG） \
        OPPO \
        小米（MI） \
        诺基亚（NOKIA） \
        HTC \
        vivo \
        摩托罗拉（Motorola） \
        华为（HUAWEI） \
        索尼（SONY） \
        苹果（Apple） \
        魅族（MEIZU） \
        "
    list1="小米（MI）"
    return list.split(" ")
def get_phone_collection(collection_name):
    '''
    get the comemnt and tag belong to phone
    DATA_SIZE everytime
    '''
    jd_db = get_jd_db()
    collection = jd_db[collection_name]
    return collection


def get_collection(collection_name):
    '''
    get the comemnt and tag belong to phone
    DATA_SIZE everytime
    '''
    jd_db = get_jd_db()
    collection = jd_db[collection_name]
    return collection
def get_one_logo_item_id(logo,collection_goods_detail):
    data_set = collection_goods_detail.find({
                                'category.0':"手机",
                                'category.1':"手机通讯",
                                'category.2':"手机",
                                'category.3':logo},
                                limit=2
                                )
    if data_set:
        print logo
        print 'data_set: ',data_set.count()
    logo_item_id=set()
    for item in data_set:
        logo_item_id.add(item["item_id"])
    return logo_item_id
def get_item_id_comment(item_id,collection_goods_comment):
    one_item_comment_set = collection_goods_comment.find(
                                                         {'item_id':item_id},
                                                          limit=100
                                                         )
    print "one item comment set: ",one_item_comment_set.count()
    return one_item_comment_set

def get_one_logo_comment(logo,collection_goods_detail,collection_goods_comment):
    logo_comment_list =[]
    item_id_set = get_one_logo_item_id(logo,collection_goods_detail)
    for item_id in item_id_set:
        for comment in get_item_id_comment(item_id,collection_goods_comment):
            comm = Comment()
            comm.set_comm_content(comment["comm_content"])
            comm.set_tags(comment['comm_tags'])
            logo_comment_list.append(comm)
                                     
    return logo_comment_list

def create_collection(collection_name):
    jd_db = get_jd_db()
    if get_collection(collection_name)==None:
        jd_db.create_collection(collection_name)
    return jd_db[collection_name]
def get_one_good_item_comment_count(comment_collection,good_id):
    one_item_comment_count = comment_collection.find({
                                    'item_id':good_id
                                    }).count()
    return one_item_comment_count
def get_one_good_all_comment(comment_collection,good_id):
    all_comment_data = comment_collection.find({
                                    'item_id':good_id
                                    })
    print 'running at : ',good_id
    data = []
    for acd_item in all_comment_data:
        sentence = acd_item['comm_content']
        sentence_id = acd_item['_id']
        new_sen = ProcessSentence.precess_sentence(sentence)
        comment = Comment()
        comment.set_comm_content(new_sen)
        comment.set_comm_id(sentence_id)
        data.append(comment)
    return data     

def insert_sentence_to_db(comment_collection,sentence,sentence_id,good_id,scorelist):
    try:
        comment_collection.insert({
                                   'item_id':good_id,
                                   'sentence_id':sentence_id,
                                    'comm_content':sentence,
                                    'score':scorelist
                                  })
    except Exception,e:
        print e
    
def insert_cluster_to_db(cluster_collection,cluster_dic,good_id):
    one_key_allitem=''
    for key in cluster_dic.keys():
        list = cluster_dic.get(key)
#         for item in list:
#             one_key_allitem+=item+' '
        cluster_collection.insert({'item_id':good_id,\
            'cluster_name':key,'comm_list':list})
        
def get_all_good_item_id(good_collection):
    all_good_item_id = good_collection.find({
                                             'category.0':"手机",
                                             'category.1':"手机通讯",
                                             'category.2':"手机",
                                             })
    ag_id_set = set()
    i=0
    for gd_item in all_good_item_id:
        i+=1
        ag_id_set.add(gd_item['item_id'])
    return ag_id_set

def get_one_item_id_comment_clusters(cluster_connection,item_id):
    all_item_clusters = cluster_connection.find({
                                                 'item_id':item_id
                                                 })
    cluster_dic={}
    for item in all_item_clusters:
        cluster_name = item['cluster_name'].encode('utf-8')
        total_num= len(item['comm_list'])
        if cluster_dic.get(cluster_name)==None:
            cluster_dic[cluster_name]=total_num
        else:
            cluster_dic[cluster_name]=cluster_dic[cluster_name]+total_num
    return cluster_dic

def add_cluster_percent_to_db(result_dic,item_id,detail_collection):
    '''
    
    :param result_dic:{'pinmu':[(good,count),(bad,count),percent]}
    :param item_id:
    :param detail_collection:
    '''
    result_list =[]
    for item in result_dic.items():
        tmp_dic={}
        tmp_dic['parameter']=item[0]
        tmp_dic['percent']=item[1][2]
        result_list.append(tmp_dic)
    json_print(result_list)
    detail_collection.update({'item_id':item_id}, {'$set' : {'rader' : result_list}})
                         
                         
                         