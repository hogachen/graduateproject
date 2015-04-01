#!/usr/bin/env python  
#encoding:utf-8 
'''
from jpype import *
import jieba.posseg as pseg
import re
import os
data = open('../MyData/i6p2.txt')
parserResult = open('../MyData/parserResult.txt','w')
pattenpre = re.compile(r'^\d*:')
jvmpath = getDefaultJVMPath()
jarpath = os.path.join(os.path.abspath('../myparser'))
startJVM(jvmpath, "-Djava.ext.dirs=%s" % jarpath)
TA = JClass('myparser.MyStanfordParser')
jd = TA()
oldsentence = data.readline()
while oldsentence:
    if oldsentence.strip(' ') == '':
        continue
    newSen = pattenpre.split(oldsentence)
    sentence=''
    if len(newSen)==2:
        sentence = newSen[1]
    else:
        sentence = newSen[0]
        
    if len(oldsentence)>1:
        print 'sentence len: ',len(sentence)
        print oldsentence
        cutsen = pseg.cut(sentence)
        linksentence = ''
        for w in cutsen:
            linksentence += w.word + ' '
        result = jd.processOneSentence(jd.lp,jd.tlp,jd.gsf,linksentence.strip(' '));
        splitedResult = result.split('#')
        print >>parserResult,linksentence
        for item in splitedResult:
            print >>parserResult,item
    oldsentence = data.readline()

shutdownJVM()
data.close()
parserResult.close()


from  jpype import *;

jvmPath = getDefaultJVMPath() 
startJVM(jvmPath, "-ea", "-Djava.class.path=..")
Test = JPackage('Test').Test     
t = Test()      
print t.add(4,8)
print t.name
shutdownJVM()
'''




from jpype import *
import os
jvmpath = getDefaultJVMPath()
jarpath = os.path.join(os.path.abspath('../myparser'))
startJVM(jvmpath, "-Djava.ext.dirs=%s" % jarpath)
TA = JClass('myparser.MyStanfordParser')
jd = TA()
a="太 大 了"
print jd.processOneSentence(jd.lp,jd.tlp,jd.gsf,a);
shutdownJVM()
