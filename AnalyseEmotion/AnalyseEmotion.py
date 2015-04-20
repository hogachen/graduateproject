#encoding:utf-8
'''
Created on Apr 2, 2015

@author: root
'''
from Utils.AnalysedComment import  *
import chardet
def search_in_grade_words_chinese(linkword,g_w_c):
    for key in g_w_c.keys():
        dic = g_w_c[key]
        if linkword in dic :
            return key
    return '0'

def search_in_comment_words(linkword,p_c_w,n_c_w,p_e_w,n_e_w):
    if linkword in p_c_w or linkword in p_e_w:
        return 1
    elif linkword in n_c_w or linkword in n_e_w:
        return -1
    return 0
def linkword_in_negetive(linkword,n_w):
    if linkword in n_w:
        return -1
    return 0
def analyse_emotion(one_comment_item,p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w):
    score = 0;
    n_or_p=1;#negative or positive 
    tendency = 0;
    grade = 1;#most more ...
    for item in one_comment_item:
        if item.tag == 'd':
            if linkword_in_negetive(item.word,n_w)!=0:
                n_or_p = -n_or_p
            elif item.word == '太' or item.word =='有点'\
            or item.word == '偏':
                tendency =tendency -3
            else:
                grade = grade + float(search_in_grade_words_chinese(item.word,g_w_c))
        if item.tag.find('a')>=0:
            tendency = tendency + search_in_comment_words(item.word,p_c_w,n_c_w,p_e_w,n_e_w)
#     print grade
#     print n_or_p
#     print tendency
#     print
    score = n_or_p * grade * tendency
    ac = AnalysedComment(one_comment_item,score)
    return ac


def analyse_original_word(linkword,linktag,p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w):
    splitlinkword = linkword.split(' ')
    splitlinktag= linktag.split(' ')
    i = 0
    for word in splitlinkword:
        
        i+=1
