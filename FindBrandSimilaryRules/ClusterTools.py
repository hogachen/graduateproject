#encoding=utf-8
'''
Created on Apr 19, 2015

@author: root
'''
def cal_every_pair_words_distance(self):
        '''
        init the self.every_pair_words_dis_dic
        '''
        if self.dic=={}:
            self.every_pair_words_dis_dic=None
            return
        keys=self.dic.keys()
        key_count=0;
        for key in keys[:len(keys)-1]:
            key_count+=1
            for sec_key in keys[key_count:]:
                dis = self.cal_two_word_dis(key,sec_key)
                if dis != 0:
                    self.every_pair_words_dis_dic[key+'@@'+sec_key]=dis
#         for item in self.every_pair_words_dis_dic.keys():
#             print item, self.every_pair_words_dis_dic.get(item)
        print 'cal_every_pair_words_distance'