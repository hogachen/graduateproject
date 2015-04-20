#encoding=utf-8
'''
Created on Apr 19, 2015

@author: root
'''
def union_stop_word():
    bai=open('../words_lib/baidu_stop_word')
    hagong=open('../words_lib/hagong_stop_word')
    chine=open('../words_lib/chine_stop_word')
    sichuan=open('../words_lib/sichuan_stop_word')
    
    dataset=set()
    for word in bai:
        dataset.add(word.strip())
    for word in hagong:
        dataset.add(word.strip())
    for word in chine:
        dataset.add(word.strip())
    for word in sichuan:
        dataset.add(word.strip())
    result= open('../MyData/union_stop_word','w')
    for item in dataset:
        print>>result,item.strip()
    result.close()
if __name__=='__main__':
    union_stop_word()
        