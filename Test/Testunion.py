'''
Created on Apr 15, 2015

@author: root
'''
def test_union():
    list1=[1,2,3]
    list2=[3,4,5]
    listunion=list(set(list1).intersection(set(list2)))
    for i in listunion:
        print  i
    
    seta=set(list1)
    setb=set(list2)
    setc = seta | setb
    setd = seta & setb
    print setc
    print setd
    print seta-setb
    print seta^setb
def test_list_cut():
    lista = [1,2,3,4]
    l=len(lista)
    print l
    print lista[l-1:]
if __name__=='__main__':
#     test_union()
    test_list_cut()