#-*-coding:utf-8-*-
from DBOperation.DBOperation import *
from DBOperation.mongo_connection import *
from ICTCLAS_Python.nlpir import *
from Utils.CountAndTag import *
import traceback
FINAL_DIC_SIZE = 1000000
DATA_SIZE=10000


class word_and_tag():
    word=''
    tag=''
    def __init__(self,word,tag):
        self.tag=tag
        self.word=word
def init_ICTCLS():
    readuserdic()
    SetPOSmap(2)

def read_stop_word():
    stop=open('../MyData/union_stop_word')
    stop_word=set()
    for word in stop:
        stop_word.add(word.strip())
    stop.close()
    return stop_word

def link_sentence(word_and_tag_list,stop_word):
    link_sentence =''
    link_tag=''
    for item in word_and_tag_list:
        if item.word in stop_word:
            continue
        link_sentence +=item.word+" "
        link_tag += item.tag+" "
    return link_sentence,link_tag 
def link_sentence_nn(word_and_tag_list):
    '''
    input:a n n t b n n n d  
    output:a nn t b nnn d
    '''
    link_sentence =''
    is_preword_n =0
    lenth = len(word_and_tag_list)
    if word_and_tag_list[0].tag=='n':
        is_preword_n=1
        link_sentence+=word_and_tag_list[0].word
    else:
        link_sentence+=word_and_tag_list[0].word+" "
    tmp_link_word ='' 
    for item in word_and_tag_list[1:lenth]:
        if item.tag == 'n':
            tmp_link_word+=item.word
            is_preword_n=1
        else:
            is_preword_n=0
            if tmp_link_word!='':
                link_sentence+=tmp_link_word+" "
            link_sentence+=item.word+" "
            tmp_link_word=''
    return link_sentence
def add_word_to_dic(link_nn_sentence,dic):
    split_nn=link_nn_sentence.strip().split(' ')
    length = len(split_nn)
    tmp_dic={}
    for i in range(length):
        tmp_dic=dic.get(split_nn[i])
        if tmp_dic==None:
                newdic={}
                dic[split_nn[i]] = newdic
                tmp_dic =dic[split_nn[i]]
        for j in range(length):
            if i == j:continue
            second_word = split_nn[j]
            count = tmp_dic.get(second_word)
            if count!= None:
                tmp_dic[second_word]=count+1
            else:
                tmp_dic[second_word]=1
                

def add_word_to_dic_window(linktag,link_nn_sentence,dic,window_size):
    split_nn=link_nn_sentence.strip().split(' ')
    split_link_tag=linktag.strip().split(' ')
    length = len(split_nn)
    if length ==0:return
    tmp_dic={}
    for i in range(length):
        tmp_dic=dic.get(split_nn[i])
        if tmp_dic==None:
                newdic={}
                dic[split_nn[i]] = newdic
                tmp_dic =dic[split_nn[i]]
        pre_index,after_index=get_window_size_index(i,length,window_size)
        for j in range(pre_index,after_index):
            if i == j:continue
            second_word = split_nn[j]
#             count = tmp_dic.get(second_word).count
            if tmp_dic.get(second_word)!= None:
                
                tmp_dic[second_word].count=tmp_dic[second_word].count+1
            else:
                try:
                    cat = CountAndTag(1,split_link_tag[j])
                    tmp_dic[second_word]=cat
                except Exception,e:
                    print 'hoga',j,i,linktag,link_nn_sentence,length
                    print e
def get_window_size_index(i,length,window_size):
    pre_index = i-window_size
    after_index = i+window_size
    if pre_index <0:pre_index = 0
    if after_index>length-1:after_index=length-1
    
    return pre_index,after_index     
def seg_line2word_and_tag_list(seg_line):
    word_and_tag_list=[]
    word_and_tag_list_list=[]
    for item in seg_line:
#         print item[0],item[1];
        if item[1].find('w') >=0 :continue
        
        wat= word_and_tag(item[0],item[1])
        
        word_and_tag_list.append(wat)
    return word_and_tag_list  

def seg_line2word_and_tag_list_mean_group(seg_line):
    '''
    split the sentence by the mean group(by tag)
    :param seg_line:
    '''
    word_and_tag_list=[]
    word_and_tag_list_list=[]
    for item in seg_line:
        if item[1].find('w') >=0 and len(word_and_tag_list)>0:
            word_and_tag_list_list.append(word_and_tag_list)
            word_and_tag_list=[]
        else:
            wat= word_and_tag(item[0],item[1])
            word_and_tag_list.append(wat)
    return word_and_tag_list_list        
       
def get_words_set(dic,comment_data,window_size,stop_word):
    i = 0
    for line in comment_data:
#         print line.content
        if i == 0:
            print len(dic)
            i=1
        if line.comm_content.strip()== '' or line.comm_content==None:
            continue
        else:
            newline = line.comm_content.encode("utf-8").replace("\n"," ")
            seg_line = Seg(newline)
        word_and_tag_list_list=seg_line2word_and_tag_list_mean_group(seg_line)
        #link_nn_sentence = link_sentence_nn(word_and_tag_list)
        for word_and_tag_list in word_and_tag_list_list:
            link_nn_sentence,linktag = link_sentence(word_and_tag_list,stop_word)
            add_word_to_dic_window(linktag,link_nn_sentence,dic,window_size)
        if len(dic) > FINAL_DIC_SIZE:
            break
    return len(dic)

    