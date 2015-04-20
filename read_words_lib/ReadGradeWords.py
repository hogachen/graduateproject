#encoding:utf-8
'''
Created on Apr 1, 2015

@author: root
'''
import chardet
def read_grade_word_file(filename):
    number = ['0','1','2','3','4','5','6','7','8','9']
    grade_dic = {}
    ofile = open(filename)
#     print 'int read grade words ',chardet.detect(line),type(line)
#     line8 = line.decode('utf-8').encode('utf-8')
#     print 'line8 :',type(line8),chardet.detect(line8)
#     print "1.most" == line.strip()
    grade_key=''
    for line in ofile:
        line = line.strip()
        if line[0] in number:
            split_line = line.split('#')
            one_grade_dic = []
            grade_key=split_line[1]
#             print grade_key
            grade_dic[grade_key]=one_grade_dic
            continue
        else:
            grade_dic[grade_key].append(line)
            
#         print line
    ofile.close()
#     tmp = grade_dic['1'][1]
#     print 'after :',chardet.detect(tmp),type(tmp),tmp
    return grade_dic

def read_emotion_and_comment_file(filename):
    of = open(filename)
    line = of.readline().strip()
    dic = set()
    while line:
        if line == '':
            continue
            line = of.readline().strip()
        else:
            dic.add(line)
        line = of.readline().strip()
    return dic

def init_file():
    p_c_w = read_emotion_and_comment_file('../words_lib/positive_comment_words') 
    n_c_w = read_emotion_and_comment_file('../words_lib/negative_comment_words')
    p_e_w = read_emotion_and_comment_file('../words_lib/positive_emotion_words')
    n_e_w = read_emotion_and_comment_file('../words_lib/negative_emotion_words')
    g_w_c = read_grade_word_file('../words_lib/grade_words_chinese.txt')
    n_w = read_emotion_and_comment_file('../words_lib/negative_words')
    if len(p_c_w)<10:
        print 'init words lib failed'
    else:
        print len(p_c_w),len(n_c_w),len(p_e_w),len(n_e_w),len(g_w_c),len(n_w)
    return p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w