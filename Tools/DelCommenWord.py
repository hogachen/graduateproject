#encoding
'''
Created on Apr 8, 2015

@author: root
'''
class WordFulAndTotalTimes():
    word=''
    times=0.0
    total_times = 0.0
    def __init__(self,word,times,total_times):
        self.word=word
        self.times=times
        self.total_times = total_times
        
        
class DelCommenWord():
    dic_times ={}
    dic_total_times={}
    def __init__(self):
        pass
    
    def cal_times_totaltimes(self,list):
        if len(list)==0:return
        for itemsplit in list:
            item = itemsplit.split("#")
            if self.dic_times.get(item[0])==None and self.dic_total_times.get(item[0])==None:
                self.dic_times[item[0]] = 1
                self.dic_total_times[item[0]]=float(item[1])
            else:
                self.dic_times[item[0]]=self.dic_times.get(item[0])+1
                self.dic_total_times[item[0]]= self.dic_total_times[item[0]]+float(item[1])
    def read_data(self,filename):
        fi=open(filename)
        i=0
        for line in fi:
            i+=1
            if i==10:
                pass
            if line.strip()=="":continue
            if line.find("#")>=0:
                list = line.split(" ")
                self.cal_times_totaltimes(list)
    def sort_dic(self,dic):
        return sorted(dic.items(), key=lambda a: a[1],reverse=True)
#         sorted(self.dic_total_times.items(),key=lambda a:a[1],reverse=True)
    def print_dic(self,outfile,outfile2):
        of = open(outfile,'w')
        outfile2=open(outfile2,'w')
        dic_time=self.sort_dic(self.dic_times)
        for item in dic_time:
            print >>of,'%-15s %10.1f' %(item[0],item[1])
        dic_total_time = self.sort_dic(self.dic_total_times)
        for item in dic_total_time:
            print >>of,'%-15s %-10.2f' %(item[0],item[1])
        
        
    def compute(self,infile,outfile):
        self.read_data(infile)
        self.print_dic(outfile)
        
    def gen_union_set(self,file_dic1,file_dic2,outfile):
        file_dic1 = open(file_dic1)
        file_dic2=open(file_dic2)
        outfile = open(outfile,'w')
        
        num=200
        i=0
        a=[]
        b=[]
        for item in file_dic1:
            i+=1
            if i> num:
                break
            a.append(item.split(" ")[0].strip())
        i=0
        for item in file_dic2:
            i+=1
            if i> num:
                break
            b.append(item.split(" ")[0].strip())
        and_set =list(set(a).union(set(b)))
        for word in and_set:
            print>>outfile,word
        file_dic1.close()
        file_dic2.close()
        outfile.close()
        
    def gen_and_set(self,file_dic1,file_dic2,outfile):
        file_dic1 = open(file_dic1)
        file_dic2=open(file_dic2)
        outfile = open(outfile,'w')
        
        num=200
        i=0
        a=[]
        b=[]
        for item in file_dic1:
            i+=1
            if i> num:
                break
            a.append(item.split(" ")[0].strip())
        i=0
        for item in file_dic2:
            i+=1
            if i> num:
                break
            b.append(item.split(" ")[0].strip())
        for word in a:
            if word in b:
                print>>outfile,word
        file_dic1.close()
        file_dic2.close()
        outfile.close()
        
    def gen_similary_word(self,simliary_dic,and_set,of):
        of = open(of,'w')
        fi=open(simliary_dic)
        and_fi=open(and_set)
        commen_list =[]
        for item in and_fi:
            commen_list.append(item.split(" ")[0].strip())
        i=0
        for line in fi:
            
            if line.strip()=="":continue
            if line.find("#")>=0:
                i+=1
                if i==3:
                    list = line.split(" ")
                    self.del_com_word(list,commen_list,of)
                    break
    def del_com_word(self,list,commen_list,of):
        for item in list:
            word = item.split("#")[0].strip()
            if word not in commen_list:
                print >>of,word
if __name__=="__main__":
#     infile = "../MyData/similary_dic"
#     outfile="../MyData/del_word"
#     outfile2="../MyData/set_word"
    dcw=DelCommenWord()
#     dcw.compute(infile,outfile)
    
#     infile = "../MyData/del_file1"
#     infile2="../MyData/del_file2"
#     outfile="../MyData/and_set"
#     dcw.gen_and_set(infile,infile2,outfile)
    
    
    similary_dic = "../MyData/similary_dic"
    and_set="../MyData/and_set"
    of="../MyData/one_line_special_word"
    dcw.gen_similary_word(similary_dic,and_set,of)
        
                
