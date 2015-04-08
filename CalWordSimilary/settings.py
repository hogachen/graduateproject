# -*- coding: utf-8 -*-

# Scrapy settings for jdspider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jdspider'

SPIDER_MODULES = ['jdspider.spiders']
NEWSPIDER_MODULE = 'jdspider.spiders'



ITEM_PIPELINES = {
    'jdspider.pipelines.mongodb.MongodbGoodsPipeline' : 100,
    'jdspider.pipelines.mongodb.MongodbCommentsPipeline': 200
}




# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jdspider (+http://www.yourdomain.com)'



RANDOMIZE_DOWNLOAD_DELAY = True


#LOG 配置
LOG_FILE = "scrapy.log" 
LOG_LEVEL = "INFO"   #可选的级别有: CRITICAL、 ERROR、WARNING、INFO、DEBUG


#
# SETTINGS_PRIORITIES = {
#     'default': 0,
#     'command': 10,
#     'project': 20,
#     'cmdline': 40,
# }

#配置MONGO数据库地址、帐号、密码
SINGLE_MONGODB_SERVER = "192.168."
SINGLE_MONGODB_PORT = 27017
SINGLE_MONGODB_DB = "jd_item"
SINGLE_MONGODB_USER = "mitch"
SINGLE_MONGODB_PASSWORD = "88888"

#配置redis地址和端口
REDIS_SERVER = "127.0.0.1"
REDIS_PORT = 6379

#设置抓评论的爬虫一次爬取处理多少商品
#测试的话可以设置小一点1-20
#正式工作可以设置为3000以上
PER_CRAWL_ITEM_COUNT = 10000

