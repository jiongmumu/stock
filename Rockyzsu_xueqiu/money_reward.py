# -*-coding=utf-8-*-

# @Time : 2018/10/23 9:26
# @File : money_reward.py
import requests
from collections import OrderedDict
import time
import datetime
import pymongo
import config
db = pymongo.MongoClient('10.18.6.26', 27001)
doc = db['db_parker']['xueqiu_reward1']
failed_doc = db['db_parker']['xueqiu_reward_status1']

session = requests.Session()
def get_proxy(retry=10):
    proxyurl = 'http://{}:8081/dynamicIp/common/getDynamicIp.do'.format(config.PROXY)
    count = 0
    for i in range(retry):
        try:
            r = requests.get(proxyurl, timeout=10)
        except Exception as e:
            print(e)
            count += 1
            print('代理获取失败,重试' + str(count))
            time.sleep(1)

        else:
            js = r.json()
            proxyServer = 'http://{0}:{1}'.format(js.get('ip'), js.get('port'))
            proxies_random = {
                'http': proxyServer
            }
            return proxies_random


def get_content(url):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.2.1120330993.1533803771; device_id=45dc0a51a26fc3078e5d8636d5141178; aliyungf_tc=AQAAABUPpRGD+w0AOnFoypiKi1AgLha3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1538060166,1539759418; s=ev17xxecme; _gid=GA1.2.489835841.1540172180; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=0a093a7b60eeaf5abb3468ebb1827ab37492829a; xq_a_token.sig=Ugrl-_BEM5Ed2K1tThP4B9xd-WI; xqat=0a093a7b60eeaf5abb3468ebb1827ab37492829a; xqat.sig=cC3oDwhUgpI-cY_nx4o-fIir8ag; xq_r_token=7147aa65f965bdfd68872710923386e22d547761; xq_r_token.sig=WZ_zkORdsy2K2ngXNlFRV6DkcCg; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=1733473480; u.sig=2sMTnVmBVOASyCZs6lbVBQ6Zfgs; bid=a8ec0ec01035c8be5606c595aed718d4_jnl1zufy; _gat_gtag_UA_16079156_4=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1540258247",
        "Host": "xueqiu.com",
        "Pragma": "no-cache",
        "Referer": "https://xueqiu.com/2227798650/115496801",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    try:
        proxy = get_proxy()
    except Exception as e:
        print(e)
        proxy = get_proxy()

    try:
        r = session.get(url=url, headers=headers,proxies=proxy,timeout=10)
    except Exception as e:
        print(e)
        proxy = get_proxy()
        r = session.get(url=url, headers=headers,proxies=proxy,timeout=10)

    return r


def parse_content(post_id):
    url = 'https://xueqiu.com/statuses/reward/list_by_user.json?status_id={}&page=1&size=99999999'.format(post_id)
    r = get_content(url)
    print('post id {}'.format(post_id))
    print(r.text)
    if r.status_code != 200:
        print('status code != 200')
        failed_doc.insert({'post_id':post_id,'status':0})
        return None

    try:

        js_data = r.json()
    except Exception as e:
        print(e)
        print('can not parse to json')
        print(post_id)
        failed_doc.insert({'post_id': post_id, 'status': 0})
        return

    ret = []
    been_reward_user = '元卫南'
    for item in js_data.get('items'):
        name = item.get('name')
        amount = item.get('amount')
        description = item.get('description')
        user_id = item.get('user_id')
        created_at = item.get('created_at')
        if created_at:
            created_at = datetime.datetime.fromtimestamp(int(created_at) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        d = OrderedDict()
        d['name'] = name
        d['user_id'] = user_id
        d['amount'] = amount / 100
        d['description'] = description
        d['created_at'] = created_at
        d['been_reward'] = been_reward_user
        d['origin_post_id']=post_id
        ret.append(d)

    # print(ret)
    print('len of ret {}'.format(len(ret)))
    if ret:
        doc.insert_many(ret)
        failed_doc.insert({'post_id':post_id,'status':1})
    else:
        failed_doc.insert({'post_id':post_id,'status':-1})




def get_all_page_id(user_id):
    doc = db['db_parker']['xueqiu_zhuanglan']

    get_page_url = 'https://xueqiu.com/statuses/original/timeline.json?user_id={}&page=1'.format(user_id)
    r = get_content(get_page_url)
    max_page = int(r.json().get('maxPage'))

    for i in range(1, max_page + 1):
        url = 'https://xueqiu.com/statuses/original/timeline.json?user_id=2227798650&page={}'.format(i)
        r = get_content(url)
        js_data = r.json()
        ret = []

        for item in js_data.get('list'):
            d = OrderedDict()

            d['article_id'] = item.get('id')
            d['title'] = item.get('title')
            d['description'] = item.get('description')
            d['view_count'] = item.get('view_count')
            d['target'] = 'https://xueqiu.com/' + item.get('target')
            d['user_id']= item.get('user_id')
            d['created_at'] = datetime.datetime.fromtimestamp(int(item.get('created_at')) / 1000).strftime(
                '%Y-%m-%d %H:%M:%S')

            ret.append(d)
        print(d)
        doc.insert_many(ret)

def loop_page_id():
    doc = db['db_parker']['xueqiu_zhuanglan']
    ret = doc.find({},{'article_id':1})
    failed_ret = failed_doc.find({'status':1})
    article_id_list =[]
    for i in failed_ret:
        article_id_list.append(i.get('article_id'))

    for item in ret:
        article_id = item.get('article_id')
        print(article_id)
        article_id_list=[]
        if article_id in article_id_list:
            continue
        else:
            parse_content(article_id)


# post_id = '115496801'
# parse_content(post_id)
# user_id='2227798650'
# get_all_page_id(user_id)
loop_page_id()