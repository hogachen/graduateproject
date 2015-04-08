#encoding:utf-8
'''
Created on Apr 2, 2015

@author: root
'''
import sys
from ChineParser.AnalyseEmotion import *
from read_words_lib.ReadGradeWords import *
import unittest
class TestReadGradeWords(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testReadGradeFile(self):
        #print sys._getframe().f_code.co_name
        grade_dic = read_grade_word_file('../words_lib/grade_words_chinese.txt')
        self.assertEqual(len(grade_dic),6)
    def testReadEmotionAndCommentFile(self):
        CAE_dic = read_emotion_and_comment_file('../words_lib/negative_comment_words')
        self.assertEqual(len(CAE_dic),3118)
    def testsearch_in_grade_words_chinese(self):
        p_c_w,n_c_w,p_e_w,n_e_w,g_w_c,n_w = init_file()
        score = search_in_grade_words_chinese('很',g_w_c);
        self.assertEqual(score, '4.0')
if __name__ == '__main__':
     unittest.main()       
        