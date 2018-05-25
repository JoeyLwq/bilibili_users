# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as py

class BilibiliPipeline(object):
    def process_item(self, item, spider):
        try:
            conn = py.connect(host='127.0.0.1',user='root',passwd='123456',db='test',charset='utf8')
            cursor = conn.cursor()
            create_table = '''create table if not exists bilibili_users(archiveview varchar(10),
            article varchar(10),birthday varchar(10),coins varchar(10),
            follower varchar(10),following varchar(10),level varchar(10),
            mid int primary key,name varchar(20),officialverify_desc varchar(100),
            officialverify_type varchar(10),rank varchar(10),regtime varchar(30),
            sex varchar(3),sign varchar(100),spacesta varchar(10),
            toutu varchar(100),toutuid varchar(10),vipstatus varchar(10),
            viptype varchar(10));
            '''
            cursor.execute(create_table)
            insert = '''
            insert into bilibili_users(archiveview,article,birthday,coins,
            follower,following,level,mid,name,officialverify_desc,officialverify_type,rank,
            regtime,sex,sign,spacesta,toutu,toutuid,vipstatus,viptype) values
            ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
            '%s','%s','%s','%s','%s','%s','%s','%s');
            ''' %(item['archiveview'],item['article'],item['birthday'],item['coins'],
             item['follower'],item['following'],item['level'],
            item['mid'],item['name'],item['officialverify_desc'],item['officialverify_type'],
             item['rank'],item['regtime'],item['sex'],item['sign'],item['spacesta'],
            item['toutu'],item['toutuid'],item['vipstatus'],item['viptype'])
            cursor.execute(insert)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(e,item['mid'])



