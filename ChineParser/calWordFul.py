#encoding:utf-8
'''
Created on Mar 30, 2015

@author: root
'''
from getAttrNN import import *

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
    return calwordful