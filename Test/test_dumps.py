#encoding=utf-8
'''
Created on Apr 20, 2015

@author: root
'''
import json
from Tools.easy_print import *
def test_dumps():
    a={1:1,'a':'曝光'}
    l=[1,3,54,'曝光','d']
    print a
    json_print(a)
    print json.dumps(l, encoding="utf-8", ensure_ascii=False)
if __name__=='__main__':
    test_dumps()