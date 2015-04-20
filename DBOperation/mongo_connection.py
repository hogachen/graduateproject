#encoding=utf-8

from pymongo import MongoClient
import traceback


class MongoConnection(object):
    db=None
    def __init__(self):
        
        self.MONGODB_SERVER = "192.168.202.231" 
        self.MONGODB_PORT = 55444
        self.MONGODB_DB = "jd_item"
        self.MONGODB_USER = "mitch"
        self.MONGODB_PASSWORD = "88888"
        
        try:            
            self.client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)            
            self.db = self.client[self.MONGODB_DB]
            self.db.authenticate(self.MONGODB_USER, self.MONGODB_PASSWORD)
        except Exception:
            traceback.print_exc()
            
    def getConnection(self):
        return self.client
    
    '''
        返回jd_item数据库链接
    '''
    def getJDDB(self):
        return self.db