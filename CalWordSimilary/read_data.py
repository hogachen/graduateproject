#-*-coding:utf-8-*-
from DBOperation import *
from mongo_connection import *
from ICTCLAS_Python.nlpir import *
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

def link_sentence(word_and_tag_list):
    link_sentence =''
    for item in word_and_tag_list:
        link_sentence +=item.word+" "
    return link_sentence        
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
def seg_line2word_and_tag_list(seg_line):
    word_and_tag_list=[]
    
    for item in seg_line:
#         print item[0],item[1];
        if item[1].find('w') >=0 :continue
        
        wat= word_and_tag(item[0],item[1])
        
        word_and_tag_list.append(wat)
    return word_and_tag_list        
       
def get_words_set(dic,comment_data):
    i = 0
    for line in comment_data:
#         print line.content
        if i == 0:
            print len(dic)
            i=1
        if line.content.strip()== '' or line.content==None:
            continue
        else:
            newline = line.content.encode("utf-8").replace("\n"," ")
            seg_line = Seg(newline)
        word_and_tag_list=seg_line2word_and_tag_list(seg_line)
        #link_nn_sentence = link_sentence_nn(word_and_tag_list)
        link_nn_sentence = link_sentence(word_and_tag_list)
        add_word_to_dic(link_nn_sentence,dic)
        if len(dic) > FINAL_DIC_SIZE:
            break
    return len(dic)

    