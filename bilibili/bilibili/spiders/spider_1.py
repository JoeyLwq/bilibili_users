# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import json
from bilibili.items import BilibiliItem
import time
import requests
import random

class Spider1Spider(scrapy.Spider):
    name = 'spider_1'
    allowed_domains = ['bilibili.com']
    url = 'https://space.bilibili.com/ajax/member/GetInfo'
    head = {

            'Accept': 'application/json,text/plain,*/*',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'space.bilibili.com',
            'Origin': 'https://space.bilibili.com',
            'Referer': 'https://space.bilibili.com/%d/' % random.randint(1,1000),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    def start_requests(self):  # 模拟成浏览器访问
        form_data = {
            'mid': '1',
            'csrf': '',
        }
        yield FormRequest(url=self.url, headers=self.head,method='POST',callback=self.parse,formdata=form_data)

    def parse(self, response):

        item = BilibiliItem()
        content = json.loads(response.body)
        data = content['data']

        try:
            item['status'] = content['status'] if 'status' in data.keys() else 'False'
            item['mid'] = data['mid']
            item['name'] = data['name']
            item['sex'] = data['sex']
            item['rank'] = data['rank']
            item['face'] = data['face']
            try:
                item['regtime'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(data['regtime']))
            except:
                item['regtime'] = 'miss'
            item['spacesta'] = data['spacesta']
            item['birthday'] = data['birthday'] if 'birthday' in data.keys() else 'miss'
            item['sign'] = data['sign']
            item['level'] = data['level_info']['current_level']
            item['officialverify_type'] = data['official_verify']['type']
            item['officialverify_desc'] = data['official_verify']['desc']
            item['viptype'] = data['vip']['vipType']
            item['vipstatus'] = data['vip']['vipStatus']
            item['toutu'] = data['toutu']
            item['toutuid'] = data['toutuId']
            item['coins'] = data['coins']
            print('successful1 get userinfo:' + str(data['mid']))
        except Exception as e:
            print('error1:',item['mid'],e)

        try:
            header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                      'Accept-Encoding': 'gzip, deflate, br',
                      'Accept-Language': 'zh-CN,zh;q=0.9',
                      'Cache-Control': 'max-age=0',
                      'Connection': 'keep-alive',
                      'Cookie': 'sid=kh3nfx8z; UM_distinctid=160f901ca0540-077f672036c946-3c604504-130980-160f901ca061d; buvid3=18869AAC-BC92-43DF-8929-333117E24C5231000infoc; fts=1516006134; LIVE_BUVID=AUTO5115160061339503; pgv_pvi=7086867456; rpdid=oqxiqwmllodosomkwxoxw; finger=edc6ecda',
                      'Host': 'api.bilibili.com',
                      'Upgrade-Insecure-Requests': '1',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
            url1 = 'https://api.bilibili.com/x/relation/stat?vmid=%d&jsonp=jsonp' %int(data['mid'])
            content1 = json.loads(requests.get(url=url1,headers=header).text)
            item['following'] = content1['data']['following']
            item['follower'] = content1['data']['follower']
            url2 = 'https://api.bilibili.com/x/space/upstat?mid=%d&jsonp=jsonp' %int(data['mid'])
            content2 = json.loads(requests.get(url=url2,headers=header).text)
            item['archiveview'] = content2['data']['archive']['view']
            item['article'] = content2['data']['article']['view']
            print('successful2 get userinfo:' + str(data['mid']))
        except Exception as e:
            item['following'] = 0
            item['follower'] = 0
            item['archiveview'] = 0
            item['article'] = 0
            print('miss2:',item['mid'],e)

        yield item
        for i in range(2,100):
            form_data = {
                'mid': str(i),
                'csrf': '',
            }
            yield FormRequest(url=self.url,callback=self.parse,headers=self.head,formdata=form_data)









