#!/usr/bin/env python  
#encoding:utf-8 
'''
Created on Mar 27, 2015

@author: root
'''

from nlpir import *

#设置词性标注集
SetPOSmap(2) 

#调用nlpir.py中的Seg（）函数，对字符串分词
p = '国家主席习近平4月11日到湖北省武汉市考察工作。'
print p
p = p.encode('UTF8')
print(p)
s=''
for t in Seg(p):
    s+= '%s/%s' % (t[0],t[1])
print(s)