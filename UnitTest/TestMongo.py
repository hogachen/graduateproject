#encoding:utf-8
'''
Created on Apr 5, 2015

@author: root
'''
from FindBrandSimilaryRules.read_data import *
from ICTCLAS_Python.nlpir import *
import unittest
class TestMongo(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        pass
#     def testMongoConnection(self):
#         result = get_phone_data()
#         self.assertEqual(len(result),0)
    def testlink_sentence_nn(self):
        init_ICTCLS()
        seg_line = Seg("手机内存也够用手机内存也够用")
        word_and_tag_list=seg_line2word_and_tag_list(seg_line)
        lsnn=link_sentence_nn(word_and_tag_list)
        self.assertEqual(lsnn,"手机内存 也 够用 手机内存 也 够用 ")
        dic={}
        add_word_to_dic(lsnn,dic)
        self.assertEqual(len(dic),3)
    def testSpecialSen(self):
        init_ICTCLS()
        seg_line = Seg("售后服务性价比也够用")
        for item in seg_line:
            print item[0],item[1]
        seg_line2word_and_tag_list(seg_line)
if __name__=="__main__":
    unittest.main()
        
        