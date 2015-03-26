#!/usr/bin/env python  
#encoding:utf-8 

from jpype import *
import os
jvmpath = getDefaultJVMPath()
jarpath = os.path.join(os.path.abspath('../myparser'))
startJVM(jvmpath, "-Djava.ext.dirs=%s" % jarpath)
TA = JClass('myparser.MyStanfordParser')
jd = TA()
a="这 是 第一 个 测试 句子 。"
jd.processOneSentence(jd.lp,jd.tlp,jd.gsf,a);
shutdownJVM()

'''
from  jpype import *;

jvmPath = getDefaultJVMPath() 
startJVM(jvmPath, "-ea", "-Djava.class.path=..")
Test = JPackage('Test').Test     
t = Test()      
print t.add(4,8)
print t.name
shutdownJVM()
'''