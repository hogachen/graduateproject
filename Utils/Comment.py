#encoding=utf
'''
Created on Apr 11, 2015

@author: root
'''

class Comment():
    comm_content=None
    comm_id = None
    tags = ''
    others=''
    def __init__(self):
        pass
    def set_comm_content(self,comm_content):
        '''
        :param comm_content:comment content
        '''
        self.comm_content = comm_content
    def set_comm_id(self,comment_id):
        '''
        :param comment_id:comment id
        '''
        self.comm_id = comment_id
    def set_tags(self,tags):
        self.tags = tags
    def set_others(self,others):
        self.others = others
