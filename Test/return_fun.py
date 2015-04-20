'''
Created on Apr 18, 2015

@author: root
'''
class test():
    s=None
    l=None
    def __init__(self):
        self.s=set()
        self.l=[]
    
def test_return():
    list=[1,2,3,4]
    return list
if __name__=='__main__':
    cl=[]
    cs=set()
    for i in range(3):
        t=test()
        t.s.add(i)
        t.l.append(2)
        cl.append(t)
    for item in cl:
        print len(item.s)
        print len(item.l)
        print
        
def test_new_windo0w():
    pass

