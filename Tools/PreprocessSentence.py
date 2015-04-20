#encoding=utf-8
'''
Created on Apr 11, 2015

@author: root
'''
class ProcessSentence():
    def __init__(self):
        pass
    @staticmethod
    def precess_sentence(sentence):
        try:
            new_sen = sentence.strip()
            new_sen2= new_sen.replace('\n','')
            return new_sen2.encode("utf-8")
        except (RuntimeError, ), e:
            raise