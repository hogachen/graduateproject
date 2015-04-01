#encoding:utf-8
'''
Created on Mar 30, 2015

@author: root
get attrtube NN N of the item
'''

import re
def getAttr(linktag,linkword):
    wordwithtag = {}
    NNpatten = re.compile(r'n n')
    Npatten = re.compile(r'n')
    linktagsplit = linktag.split(' ')
    linkwordsplit = linkword.split(' ')
    haveNN = 0
    for match in NNpatten.finditer(linktag):
        haveNN =1
        a = linkwordsplit[match.start()]+" "+linkwordsplit[match.end()-2]
        print a
        wordwithtag[a]=linktag
        print wordwithtag[a]
    if haveNN == 0:
        for Nmatch in Nmatch.finditer(linktag):
            print Nmatch.start()
        
        
def getAttr2(linktag,linkword):
    wordwithtag = {}
    wordwithtag2=[]
    linktagsplit = linktag.split(' ')
    linkwordsplit = linkword.split(' ')
    tagandword =''
    i=0
    for tag in linktagsplit:
        if tag == 'n':
            tagandword+=linkwordsplit[i]+' '
        else:
            newtw = tagandword.strip(' ')
            if newtw!='':
                wordwithtag2.append(newtw)
            tagandword = ''
        i+=1
#     for word in wordwithtag2:
#         print word
    return wordwithtag2



    
if __name__ == '__main__':
    string = '但是 售 后 的 解决 结果 非常 不 满意'
    linktag ='n n d n n d n sa'
    getAttr2(linktag,string)
