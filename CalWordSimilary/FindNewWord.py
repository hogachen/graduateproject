#encoding=utf-8
'''
Created on Apr 6, 2015

@author: root
'''
from ICTCLAS_Python.nlpir import *
from read_data import *
class FindNewWord():
    def __init__(self):
        init_ICTCLS()
        pass
    
    def find_new_word(self,sentence):
        seg_sentence = Seg(sentence)
        print seg_sentence
        for item in seg_sentence:
            print item[1],item[0]
        print GetNewWords(sentence,50,"false")
#         return new_word_list


if __name__ == "__main__":
    fnw = FindNewWord()
    fnw.find_new_word("妹纸肿么回事")