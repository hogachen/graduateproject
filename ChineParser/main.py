#encoding:utf-8
'''
Created on Mar 30, 2015

@author: root
'''
from getAttrNN import *
import re
def calwordful():
    attfile = open('../MyData/matchdata')
    linktag = attfile.readline()
    linkword = ''
    calwordful ={}
    while linktag:
        linkword = attfile.readline()
        tandw = getAttr2(linktag,linkword)
    
        for item in tandw:
            if item in calwordful.keys():
                calwordful[item]=calwordful[item]+1
            else:
                calwordful[item]=1
    
        linktag = attfile.readline()
    
    attfile.close()
    
def test_re_patten(sentence):
    splitw = sentence.split('w')
    for item in splitw:
        print item
if __name__ == '__main__':
    test_re_patten('a n d c')
        
    