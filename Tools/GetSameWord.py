#encoding=utf-8
'''
Created on Apr 10, 2015

@author: root
'''
class OtherOperation():
    def __init__(self):
        pass
    
    def get_same_word_in_comment_word(self,pfile,nfile,outfile):
        nfile=open(nfile)
        pfile=open(pfile)
        of=open(outfile,'w')
        list=[]
        for p_item in pfile:
            list.append(p_item)
        for item in nfile:
            if item in list:
                print >>of,item,
        of.close()
        nfile.close()
        pfile.close()
if __name__ == "__main__":
    oo= OtherOperation()
    pfile="../words_lib/positive_comment_words"
    nfile="../words_lib/negative_comment_words"
    outfile="../words_lib/unit_comment_word"
    oo.get_same_word_in_comment_word(pfile, nfile, outfile)
    
    
    
    
    