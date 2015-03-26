'''
Created on Mar 22, 2015

@author: hoga
'''
print "hello"
import re
import jieba.posseg as pseg
from WordAndTag import wordandtag
#read data rom  text
data = open("../Data/i6p2.txt")
of = open("../Data/result.txt",'w')
oldsentence = data.readline()
nbapatten = re.compile(r"n .*?a")
pattenpre = re.compile(r'^\d*:')
while oldsentence:
    if oldsentence.strip(' ') == '':
        continue
    newSen = pattenpre.split(oldsentence)
    sentence=''
    if len(newSen)==2:
        sentence = newSen[1]
    else:
        sentence = newSen[0]
        
    #for debug and can delete after  
    sentence2 = sentence.strip('\n')
    words=pseg.cut(sentence2)
    sentenceWithTag =''
    for w in words:
        sentenceWithTag+=w.word+' '+w.flag+' '
    
    words=pseg.cut(sentence)
    linktag = ''
    linkword = ''
    for word in words:
        if word.flag != 'x':
            linkword += word.word+' '
            linktag+=word.flag+' '
        else:
            if linkword.strip(' ') != '':
                nbamatch = nbapatten.match(linktag)
                if nbamatch:
                    print  >>of,'[useful]',linkword,linktag
                linktag=''
                linkword=''
    print >>of,sentenceWithTag+'\n'
    oldsentence=data.readline()
data.close()
of.close()





'''
import jieba.posseg as pseg
#read data rom  text
data = open("../Data/data.txt")
sentence = data.readline()
while sentence:
    print sentence
    words=pseg.cut(sentence)
    linktag = ''
    for word in words:
        linktag+=word.flag
        linktag+=' '
    print linktag
    splitwithx = linktag.split('x')
    for splitedsentag in splitwithx:
        if splitedsentag.strip(' ')!='':
            print splitedsentag.strip(' ')
    sentence=data.readline()
data.close()





import re
import jieba.posseg as pseg
from WordAndTag import wordandtag
#read data rom  text
data = open("../Data/i6p2.txt")
of = open("../Data/result.txt",'w')
oldsentence = data.readline()
allSentenceList = [[]]
while oldsentence:
    if oldsentence.strip(' ') == '':
        continue
    #print >> of,oldsentence
    pattenpre = re.compile(r'^\d*:')
    newSen = pattenpre.split(oldsentence)
    sentence=''
    if len(newSen)==2:
        sentence = newSen[1]
    else:
        sentence = newSen[0]
    oneSentenceList=[]
    words=pseg.cut(sentence)
    linktag = ''
    linkword = ''
    for word in words:
        if word.flag != 'x':
            linkword += word.word+' '
            linktag+=word.flag+' '
        else:
            if linkword.strip(' ') != '':
                wat = wordandtag(linkword,linktag)
                oneSentenceList.append(wat) 
                linktag=''
                linkword=''
    #print >>of,linktag
    
    allSentenceList.append(oneSentenceList)
    oldsentence=data.readline()
data.close()
print >>of,len(allSentenceList)

nbapatten = re.compile(r"n.*?a")#"n.*?d.*?a"
for splitedSen in allSentenceList:
    for onesplitedsen in splitedSen:
        #print onesplitedsen.linkword,onesplitedsen.linktag
        nbamatch = nbapatten.match(onesplitedsen.linktag)
        if nbamatch:
            #print >>of,
            print >>of,onesplitedsen.linkword,onesplitedsen.linktag
#    print >>of
of.close()
'''
