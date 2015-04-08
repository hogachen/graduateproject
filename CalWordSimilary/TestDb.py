#encoding:utf-8
'''
Created on Apr 5, 2015

@author: root
'''
import pymongo
import datetime
import time
def sortedDictValues1(dic): 
    items = dic.items() 
    items.sort() 
    return sorted(dic.items(), key=lambda a: a[1]) 
#     return [ (k,v) for v in sorted(dic.values())] 
    return [value for key, value in items]  

def TimeSkip():
    starttime = datetime.datetime.now()
#     time.sleep(1)
    endtime = datetime.datetime.now()
    print "time used: %s second" %(endtime - starttime).seconds
if __name__ == "__main__":
    TimeSkip()
    dic = {'a':6 , 'd':2 , 'c': 3}
    for item in sortedDictValues1(dic):
        print item[0],item[1]