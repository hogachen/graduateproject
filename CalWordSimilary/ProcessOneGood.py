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
import chardet
from ICTCLAS_Python.nlpir import *
from SimilaryWordCluster import *
from Utils.WordAndTag import *
from AnalyseEmotion.AnalyseEmotion import *
from read_words_lib.ReadGradeWords import *
from DBOperation.DBOperation import *

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
    mark_link_sentence=[]
    
    striplinktag = linktag.strip(' ')
    striplinkword = linkword.strip(' ')
                    
    splitlinkword = striplinkword.split(' ')
    splitlinktag = striplinktag.split(' ')
    havenda = 0
    haveda  =0
    one_short_sentence =[]
    sub_one_short_sentence=[]
    for e_ndamatch in ndapatten.finditer(striplinktag):
        havenda =  1
        indexs = find_index_of_linkword(e_ndamatch.start(),e_ndamatch.end(),striplinktag)
        count = 0
        sub_one_short_sentence=[]
        for index in indexs:
            count+=1#for the vn an  nn words
            if splitlinktag[index].find('n')>=0 and count==1 and splitlinktag[index+1]=='n':
                wat = WordAndTag(splitlinkword[index]+' '+splitlinkword[index+1],splitlinktag[index]+' '+splitlinktag[index+1])
            else:
                wat = WordAndTag(splitlinkword[index],splitlinktag[index])
                sub_one_short_sentence.append(wat)
        one_short_sentence.append(sub_one_short_sentence)
        tmp_mark_sentence=''    
        mark_sentence=  splitlinkword[indexs[0]:indexs[len(indexs)-1]+1]
        for mitem in mark_sentence:
            tmp_mark_sentence+=mitem
        mark_link_sentence.append(tmp_mark_sentence) 
    if havenda == 0:
        for e_damatch in dapatten.finditer(striplinktag):
            haveda = 1
            sub_one_short_sentence = []
            indexs = find_index_of_linkword(e_damatch.start(),e_damatch.end(),striplinktag)
            for index in indexs:
                wat = WordAndTag(splitlinkword[index],splitlinktag[index])
                sub_one_short_sentence.append(wat)
            one_short_sentence.append(sub_one_short_sentence)
            tmp_mark_sentence=''    
            mark_sentence=  splitlinkword[indexs[0]:indexs[len(indexs)-1]+1]
            for mitem in mark_sentence:
                tmp_mark_sentence+=mitem
            mark_link_sentence.append(tmp_mark_sentence)
    if havenda==0 and haveda == 0: 
        for e_aornmatch in aornpatten.finditer(striplinktag):
            wat = WordAndTag(splitlinkword[0],splitlinktag[0])
            sub_one_short_sentence.append(wat)
            one_short_sentence.append(sub_one_short_sentence)
        mark_link_sentence.append(splitlinkword[0])
    if len(one_short_sentence)==0:
        return None,None
    return one_short_sentence,mark_link_sentence
    
    
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
  
  
def pre_process_sentence2(oldsentence):
     return oldsentence.strip()


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
def get_last_sentence_id():
    of = open('../MyData/last_item')
    a = of.readline().strip()
    of.close()
    return a
def read_ran_sub_item():
    of = open('../MyData/hadrun_item_id')
    item_set=set()
    for item in of:
        item_set.add(item.strip())
    of.close()
    of = open('../MyData/hadrun_item_id','w')    
    of.truncate(0)
    of.close()
    return item_set
def save_ran_item_id(sentence_id):
    subof = open('../MyData/hadrun_item_id','a')
    print>>subof,sentence_id
    subof.close()
def match_goods_att(analysed_comment_collection,clusters_collection,gid_item,one_good_all_comment,\
    p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w,swc,firsttime):
    '''
    read the data from the file and process every sentence in turn 
    '''
    cluster_dic ={}
#     
    ndapatten = re.compile(r"n .*?a")
    dapatten = re.compile(r'd .*?a')
    aornpatten = re.compile(r'^n$|^a$')
    pattenpre = re.compile(r'^\d*:')

    item_set = read_ran_sub_item()
    lastgood_id  = get_last_sentence_id()
    
    for data_item in one_good_all_comment:
        if firsttime==0 and gid_item==lastgood_id:
            if str(data_item.comm_id) in item_set:
#                 print data_item.comm_id
                continue
        
        sentence_id =data_item.comm_id
        save_ran_item_id(sentence_id)
        oldsentence =data_item.comm_content
        match_sentence_count=0
        sentence=pre_process_sentence2(oldsentence)
        
        words=Seg(sentence)
        linktag = ''
        linkword = ''
        tmptag=''
        scorelist=[]
        for word in words:
            tmptag = word[1]
            if tmptag.find('w')<0:
                linkword += word[0]+' '
                linktag+=word[1]+' '
            else:
                if linkword.strip(' ') != '':
                    sentence,match_sentence_count=analyse_short_sentence_emotion_and_cluster(match_sentence_count,\
                        linkword,linktag,ndapatten,dapatten,aornpatten,\
                        p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w,sentence,\
                        cluster_dic,swc,sentence_id,scorelist)
                    linktag=''
                    linkword=''
        '''
        some sentence have no 'w' in the final,so the last cut sentence have to proces individully 
        '''
        if tmptag.find('w')<0 and linkword.strip(' ') != '':
            sentence,match_sentence_count =analyse_short_sentence_emotion_and_cluster(match_sentence_count,\
                linkword,linktag,ndapatten,dapatten,aornpatten,\
                p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w,sentence,\
                cluster_dic,swc,sentence_id,scorelist)
        
        '''
        process one sentence over
        '''
        insert_sentence_to_db(analysed_comment_collection,sentence,sentence_id,gid_item,scorelist)      
    insert_cluster_to_db(clusters_collection,cluster_dic,gid_item)

def init_swc():
    cluster_words_file="../MyData/similary_word_n"
    swc = SimilaryWordCluster()
    swc.read_cluster_words(cluster_words_file)
    return swc


def cal_short_sentence_cluster(swc,analysed_commnet,cluster_dic,\
                               sentence_id,match_sentence_count):
#     swc.cal_sentence_cluster(analysed_commnet)
    cluster=None
    for item in analysed_commnet.one_short_sentence:
        cluster = swc.get_word_cluster(item.word,item.tag)
        if cluster !=None:
            if analysed_commnet.score != 0:
                head,good,bad=swc.cut_cluter_title(cluster)
            if analysed_commnet.score>0:
                cluster=head+good
            elif analysed_commnet.score<0:
                cluster=head+bad
            else:
                cluster=None
            break#one short_sentence must belong to only one cluster
    if cluster !=None:
        list = cluster_dic.get(cluster)
        if list != None:
            data = {}
            data['sentence_id']=sentence_id
            data['count']=match_sentence_count
            list.append(data)
        else:
            list=[]
            data = {}
            data['sentence_id']=sentence_id
            data['count']=match_sentence_count
            
            list.append(data)
            cluster_dic[cluster]=list
    return cluster,analysed_commnet.score
    
    
def analyse_short_sentence_emotion_and_cluster(match_sentence_count,\
        linkword,linktag,ndapatten,dapatten,aornpatten,\
        p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w,sentence,\
        cluster_dic,swc,sentence_id,scorelist):
    
    one_short_sentence,mark_link_sentence = get_final_good_result(linkword,\
        linktag,ndapatten,dapatten,aornpatten)
    tmp_match_count = match_sentence_count
    if one_short_sentence !=None and len(one_short_sentence)>1:
        for one_short_item in one_short_sentence:
            analysed_commnet =  analyse_emotion(one_short_item,\
                p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w)  
            cluster,score=cal_short_sentence_cluster(swc,analysed_commnet,cluster_dic,\
                sentence_id,tmp_match_count)
            scorelist.append(score)
#             print_zero_score(linkword,linktag,analysed_commnet.score,cluster)
            tmp_match_count+=1
        
    elif one_short_sentence !=None and len(one_short_sentence)==1:
        all_words = linktag_linkword(linkword,linktag)
        analysed_commnet =  analyse_emotion(all_words,\
                p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w)
        cluster,score=cal_short_sentence_cluster(swc,analysed_commnet,cluster_dic,\
                               sentence_id,match_sentence_count)
        scorelist.append(score)
#         print_zero_score(linkword,linktag,analysed_commnet.score,cluster)
    if mark_link_sentence!=None:
        for mark_item in mark_link_sentence:
            replace_str="HJT"+str(match_sentence_count)\
                +mark_item.strip()+"HJT"+str(match_sentence_count)
            sentence=sentence.replace(mark_item.strip(),replace_str)
            match_sentence_count+=1
    return sentence,match_sentence_count

def linktag_linkword(linkword,linktag):
    slw = linkword.split(' ')
    slt = linktag.split(' ')
    linktaw=''
    list =[]
    i=0
    try:
        for item in slw:
            wat = WordAndTag(slw[i],slt[i])
            list.append(wat)
            i+=1
    except Exception ,e:
        print e
    return list
def print_zero_score(linkword,linktag,score,cluster):
    
#     if score != 0:
#         return None
    if cluster==None:
        cluster='None'
    of = open('../MyData/zeroscore','a')
    i = 0
    slw = linkword.split(' ')
    slt = linktag.split(' ')
    linktaw=''
    for item in slw:
        linktaw+=item+slt[i]
        i+=1
    print >> of,linktaw,score,cluster
    of.close()
    
if __name__ == '__main__':
    match_goods_att('../MyData/data.txt')

