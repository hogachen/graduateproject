#encoding:utf-8
'''
Created on Mar 22, 2015

@author: hoga
'''
print "hello"
import re
from ICTCLAS_Python.nlpir import *
import jieba.posseg as pseg
from getAttrNN import *
from WordAndTag import *



def readuserdic():
    userword = open('../MyData/userword')
#add user word
    uword = userword.readline()
    while uword:
        AddUserWord(uword)
        uword = userword.readline()
    userword.close()


        
def find_index_of_linkword(start_index,end_index,linktag):
    if start_index==end_index:
        return 0
    index = 0
    spaceindex = 0
    startindex =-1
    midindex = -1
    endindex = -1
    while index < len(linktag):
        if linktag[index] == ' ':
            spaceindex += 1
        if index == start_index:
            startindex = spaceindex
        if start_index <index and index <end_index and linktag[index]=='d':
            midindex = spaceindex
        if(index == end_index-1):
            endindex = spaceindex
        index += 1
    if midindex == -1:
        return startindex,endindex
    else:
        return startindex,midindex,endindex


def get_final_good_result(goodresult,linkword,linktag,ndapatten,dapatten,aornpatten):
    '''
    use the regex to match the 'nad','da','n or a' patten and get the 
    tag and word which match the patten
    '''
   # print linktag,linkword
    striplinktag = linktag.strip(' ')
    striplinkword = linkword.strip(' ')
                    
    splitlinkword = striplinkword.split(' ')
    splitlinktag = striplinktag.split(' ')
    havenda = 0
    haveda  =0
    for e_ndamatch in ndapatten.finditer(striplinktag):
        havenda =  1
        indexs = find_index_of_linkword(e_ndamatch.start(),e_ndamatch.end(),striplinktag)
        one_short_sentence =[]
        count = 0
        for index in indexs:
            count+=1#for the vn an  nn words
            if splitlinktag[index].find('n')>=0 and count==1 and splitlinktag[index+1]=='n':
                wat = wordandtag(splitlinkword[index]+' '+splitlinkword[index+1],splitlinktag[index]+' '+splitlinktag[index+1])
            else:
                wat = wordandtag(splitlinkword[index],splitlinktag[index])
            one_short_sentence.append(wat)
        goodresult.append(one_short_sentence)                   
    if havenda == 0:
        for e_damatch in dapatten.finditer(striplinktag):
            haveda = 1
            one_short_sentence2 = []
            indexs = find_index_of_linkword(e_damatch.start(),e_damatch.end(),striplinktag)
            for index in indexs:
                wat = wordandtag(splitlinkword[index],splitlinktag[index])
                one_short_sentence2.append(wat)
            goodresult.append(one_short_sentence2)
    if havenda==0 and haveda == 0: 
        for e_aornmatch in aornpatten.finditer(striplinktag):
            one_short_sentence3 = []
            wat = wordandtag(splitlinkword[0],splitlinktag[0])
            one_short_sentence3.append(wat)
            goodresult.append(one_short_sentence3)    
    
def print_result(goodresult):
    of = open("../MyData/result.txt",'w')
    i =  0
    for item in goodresult:
        if  isinstance(item,str):
            i+=1
            if i == 1:
                print>>of
                print>>of,item
            if i == 2:
                print>>of,item
                i=0
            continue
        for wat in item:
            print >> of,wat.linkword,',',wat.linktag,
            print >> of,' ',
        print >>of
    of.close()
    
    
def pre_process_sentence(oldsentence,pattenpre):
    if oldsentence.strip(' ') == '':
        return ''
    newSen = pattenpre.split(oldsentence)
    sentence=''
    if len(newSen)==2:
        sentence = newSen[1]
    else:
        sentence = newSen[0]
    return sentence.strip('\n')
def match_goods_att(data_file_path):
#read data rom  text
    data = open(data_file_path)
    
    
    readuserdic()
    
    SetPOSmap(2) 
    oldsentence = data.readline()
    ndapatten = re.compile(r"n .*?a")
    dapatten = re.compile(r'd .*?a')
    aornpatten = re.compile(r'^n$|^a$')
    pattenpre = re.compile(r'^\d*:')

    goodresult = [[]]
    wares_attr = []
    while oldsentence:
        sentence=pre_process_sentence(oldsentence,pattenpre)
        if sentence == '':
            oldsentence=data.readline() 
            continue
        
    #for debug and can delete after  
        tmp = Seg(sentence)
        link_tag_word = ''
        for it in tmp:
            link_tag_word += it[0]+it[1]+' '
        goodresult.append(link_tag_word)
        
        
        goodresult.append(sentence)
        words=Seg(sentence)
        linktag = ''
        linkword = ''
        tmptag=''
        for word in words:
            tmptag = word[1]
            if tmptag.find('w')<0:
                linkword += word[0]+' '
                linktag+=word[1]+' '
            else:
                if linkword.strip(' ') != '':
                    get_final_good_result(goodresult,linkword,linktag,ndapatten,dapatten,aornpatten)
                    linktag=''
                    linkword=''
        '''
        some sentence have not a 'w' in the final,so the last cut sentence have to proces individully 
        '''
        if tmptag.find('w')<0 and linkword.strip(' ') != '':
            get_final_good_result(goodresult,linkword,linktag,ndapatten,dapatten,aornpatten)

        oldsentence=data.readline()
        
    print_result(goodresult)
    data.close()
    

if __name__ == '__main__':
    match_goods_att('../MyData/datamore.txt')






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





print "hello"
import re
import jieba.posseg as pseg
from WordAndTag import wordandtag
#read data rom  text
data = open("../Data/data.txt")
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
