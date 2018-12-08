# -*- coding: utf-8 -*-
import datetime
import scrapy
import json
from postman.items import PostmanItem


class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']

    def __init__(self):
        self.headers = {
            'Accept-Language': ' zh-CN,zh;q=0.9', 'Accept-Encoding': ' gzip, deflate, br',
            'X-Requested-With': ' XMLHttpRequest', 'Host': ' xueqiu.com', 'Accept': ' */*',
            'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
            'Connection': ' keep-alive',
            'Pragma': ' no-cache', 'Cache-Control': ' no-cache', 'Referer': ' https://xueqiu.com/u/1955602780'
        }

        self.cookies = {
            "aliyungf_tc": "AQAAAK8wUQdqBAIAOnFoykG99MSX8UP2",
            "Hm_lvt_1db88642e346389874251b5a1eded6e3": "1531100937",
            "_ga": "GA1.2.1318479403.1531100939",
            "_gid": "GA1.2.827644379.1531100939",
            "device_id": "45dc0a51a26fc3078e5d8636d5141178",
            "remember": "1",
            "remember.sig": "K4F3faYzmVuqC0iXIERCQf55g2Y",
            "xq_a_token": "3232d00d27df616b7be3fcb80531e32bb869b5a2",
            "xq_a_token.sig": "H2dYVga9uaEqSUsGhGf0L2hPDW8",
            "xq_r_token": "af52839df2ce017e2bcb613ad3112419ca5043c7",
            "xq_r_token.sig": "EWpQ-vPxGAHzmvLSp_GdhTlMHSI",
            "xq_is_login": "1",
            "xq_is_login.sig": "J3LxgPVPUzbBg3Kee_PquUfih7Q",
            "u": "1733473480",
            "u.sig": "2sMTnVmBVOASyCZs6lbVBQ6Zfgs",
            "s": "dr1846gec1",
            "bid": "a8ec0ec01035c8be5606c595aed718d4_jjdm48re",
            "Hm_lpvt_1db88642e346389874251b5a1eded6e3": "1531101192",
            "_gat_gtag_UA_16079156_4": "1",
            "snbim_minify": "true"
        }

    def start_requests(self):
        count = 20
        # userid = 9887656769
        userid = 2431057144
        # maxPage = 2
        maxPage = 856
        base_url = 'https://xueqiu.com/v4/statuses/user_timeline.json?page={}&user_id={}'
        for pn in range(1, maxPage + 1):
            url = base_url.format(pn, userid)
            yield scrapy.Request(url, cookies=self.cookies, headers=self.headers)

    def parse(self, response):
        content = json.loads(response.body_as_unicode())
        tweets = content.get('statuses', None)
        if tweets is None:
            return

        for tweet in tweets:
            item = PostmanItem()
            _id = tweet.get('id')
            userid = tweet.get('userid')
            title = tweet.get('title')
            created_at = tweet.get('created_at')
            created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000)
            retweet_count = tweet.get('retweet_count')
            reply_count = tweet.get('reply_count')
            fav_count = tweet.get('fav_count')
            truncated = tweet.get('truncated')
            commentId = tweet.get('commentId')
            symbol_id = tweet.get('symbol_id')
            description = tweet.get('description')
            source_link = tweet.get('source_link')
            user = tweet.get('user')
            target = tweet.get('target')
            timeBefore = tweet.get('timeBefore')
            text = tweet.get('text')
            source = tweet.get('source')
            retweeted_status = tweet.get('retweeted_status')
            item['_id'] = _id
            item['userid'] = userid
            item['title'] = title
            item['created_at'] = created_at
            item['retweet_count'] = retweet_count
            item['reply_count'] = reply_count
            item['fav_count'] = fav_count
            item['truncated'] = truncated
            item['commentId'] = commentId
            item['symbol_id'] = symbol_id
            item['description'] = description
            item['source_link'] = source_link
            item['user'] = user
            item['target'] = target
            item['timeBefore'] = timeBefore
            item['text'] = text
            item['source'] = source
            item['retweeted_status'] = retweeted_status
            yield item
