#encoding:utf-8
'''
Created on Mar 22, 2015
@author: hogachen
@email: 1107402232@qq.com
'''
print "hello"
import re
'''
    for the ICTCLAS have to write the data(log and error) to the ./ dir
    so I have to put the 'Data' dir at the './' dir and rm the 'ICTCLAS_Python' dir 
    'Data' dir
'''
from ICTCLAS_Python.nlpir import *
from getAttrNN import *
from WordAndTag import *
from AnalyseEmotion import *
from read_words_lib.ReadGradeWords import *
from CalWordSimilary.CalCluster import *

def readuserdic():
    userword = open('../MyData/userword')
#add user word
    uword = userword.readline()
    while uword:
        AddUserWord(uword)
        uword = userword.readline()
    userword.close()


        
def find_index_of_linkword(start_index,end_index,linktag):
    '''
        to search the index of the linkword 
        idea: use the ' ' character to split the linkword and count 
        how many ' ' character for finding the index of match sentence flag in 
        the linktag and then use the index to get the word in the splitlinkword
        example :
        sentence:给女朋友买的电池容量大！
        linkword:给 女朋友 买 的 电池 容量 大
        linktag: p n v u n n a 
        there is 4 '' character before the 'n n a' so I use  linkword[4]-linkword[6] 
        to get the wares' atttbute and comment word
        
        better method:
        to link the word and flag like this :给p 女朋友n 买v 的u 电池n 容量n 大a
        and the use the regex to match the  'n 容量n 大a' to get the word and flag
    '''
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


def get_final_good_result(linkword,linktag,ndapatten,dapatten,aornpatten):
    '''
    use the regex to match the 'nad','da','n or a' patten and get the 
    tag and word which match the patten
    use the regex patten 'n .*?a','d.*?a' ,'^n|^a' in turn to match the
    linktag
    '''
    striplinktag = linktag.strip(' ')
    striplinkword = linkword.strip(' ')
                    
    splitlinkword = striplinkword.split(' ')
    splitlinktag = striplinktag.split(' ')
    havenda = 0
    haveda  =0
    one_short_sentence =[]
    for e_ndamatch in ndapatten.finditer(striplinktag):
        havenda =  1
        indexs = find_index_of_linkword(e_ndamatch.start(),e_ndamatch.end(),striplinktag)
        count = 0
        for index in indexs:
            count+=1#for the vn an  nn words
            if splitlinktag[index].find('n')>=0 and count==1 and splitlinktag[index+1]=='n':
                wat = wordandtag(splitlinkword[index]+' '+splitlinkword[index+1],splitlinktag[index]+' '+splitlinktag[index+1])
            else:
                wat = wordandtag(splitlinkword[index],splitlinktag[index])
            one_short_sentence.append(wat)
                          
    if havenda == 0:
        for e_damatch in dapatten.finditer(striplinktag):
            haveda = 1
            one_short_sentence2 = []
            indexs = find_index_of_linkword(e_damatch.start(),e_damatch.end(),striplinktag)
            for index in indexs:
                wat = wordandtag(splitlinkword[index],splitlinktag[index])
                one_short_sentence.append(wat)
                
    if havenda==0 and haveda == 0: 
        for e_aornmatch in aornpatten.finditer(striplinktag):
            one_short_sentence3 = []
            wat = wordandtag(splitlinkword[0],splitlinktag[0])
            one_short_sentence.append(wat)
    if len(one_short_sentence)==0:
        return None
    return one_short_sentence
    
    
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
        one_short_sentence = item.one_short_sentence
        for wat in one_short_sentence:
            print >> of,wat.linkword,',',wat.linktag,
            print >> of,' ',
        print >>of,'score: ',item.score,
        print >>of
    of.close()
    
    
def pre_process_sentence(oldsentence,pattenpre):
    '''
    pre process the sentence to make the input to the userful sentence
    '''
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
    '''
    read the data from the file and process every sentence in turn 
    '''
    p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w = init_file()
    data = open(data_file_path)
    
    
    readuserdic()
    
    SetPOSmap(2) 
    
    oldsentence = data.readline()
    print type(oldsentence),chardet.detect(oldsentence)
    ndapatten = re.compile(r"n .*?a")
    dapatten = re.compile(r'd .*?a')
    aornpatten = re.compile(r'^n$|^a$')
    pattenpre = re.compile(r'^\d*:')

    goodresult = []
    wares_attr = []
    init_dic = 0
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
                    one_short_sentence = get_final_good_result(linkword,\
                        linktag,ndapatten,dapatten,aornpatten)
                    if one_short_sentence !=None:
                        analysed_commnet =  analyse_emotion(one_short_sentence,\
                            p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w)
                        goodresult.append(analysed_commnet)
                    linktag=''
                    linkword=''
        '''
        some sentence have no 'w' in the final,so the last cut sentence have to proces individully 
        '''
        if tmptag.find('w')<0 and linkword.strip(' ') != '':
            one_short_sentence = get_final_good_result(linkword,\
                linktag,ndapatten,dapatten,aornpatten)
            if one_short_sentence !=None:
                analysed_commnet =  analyse_emotion(one_short_sentence,\
                    p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w)
                goodresult.append(analysed_commnet)
            
        oldsentence=data.readline()
        
#     print_result(goodresult)
    
    
    cc = CalCluster()
    cluster_words_file="../MyData/similary_word_n"
    outfile="../MyData/short_sentence_and_cluster"
    cc.run(goodresult,cluster_words_file,outfile)
    data.close()
    return goodresult

if __name__ == '__main__':
    match_goods_att('../MyData/datamore.txt')

