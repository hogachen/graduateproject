'''
Created on Mar 31, 2015

@author: root
'''
from getAttrNN import *
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