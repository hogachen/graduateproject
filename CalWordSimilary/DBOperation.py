#encoding:utf-8
'''
Created on Apr 6, 2015

@author: root
'''
from Comment import *
from mongo_connection import *
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
    list1="小米（MI） 索尼（SONY）"
    return list.split(" ")
def get_phone_collection(collection_name):
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
                                'category.2':"手机",
                                'category.3':logo},
#                                 limit=1
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
                                                          limit=2000
                                                         )
    print "one item comment set: ",one_item_comment_set.count()
    return one_item_comment_set

def get_one_logo_comment(logo,collection_goods_detail,collection_goods_comment):
    logo_comment_list =[]
    item_id_set = get_one_logo_item_id(logo,collection_goods_detail)
    for item_id in item_id_set:
        for comment in get_item_id_comment(item_id,collection_goods_comment):
            #print comment["comm_content"]
            logo_comment_list.append(Comment(comment["comm_content"],comment['comm_tags']))
                                     
    return logo_comment_list
        
    