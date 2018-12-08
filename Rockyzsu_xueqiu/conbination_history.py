# -*-coding=utf-8-*-
import requests


class History_item():
    case = None
    cash_value = None
    category = None
    comment = None
    created_at = None
    cube_id = None
    diff = None
    error_code = None
    error_message = None
    error_status = None
    exe_strategy = None
    holdings = None
    id = None
    new_buy_count = None
    prev_bebalancing_id = None
    rebalancing_histories = None
    status = None
    updated_at = None


class DataOutput():
    def store_data(self,items):
        if isinstance(items, History_item):
            pass


class Downloader():
    def download(self, url):
        headers = {'Accept-Language': 'zh-CN,zh;q=0.9', 'Accept-Encoding': 'gzip, deflate, br',
                   'X-Requested-With': 'XMLHttpRequest', 'Host': 'xueqiu.com', 'Accept': '*/*',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                   'Connection': 'keep-alive',
                   'Cookie': 'device_id=f174304eb593fc036db5db25d3124fad; s=e31245o8yi; bid=a8ec0ec01035c8be5606c595aed718d4_j9xsz38j; isPast=; isPast.sig=b88Owy153wcLSL35qvjYa9YTRSI; __utma=1.8758030.1510556188.1513663497.1514177490.45; __utmz=1.1510556188.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); aliyungf_tc=AQAAAD9eFhuweAwACYkcDkJJBI1ot4cz; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=03c3e0da43d04f871694c6591679f2ba2d14af04; xq_a_token.sig=Atp6kVdnFUzGyfrTsT8aiNztCjE; xq_r_token=afe944bfcb3f43ba60a676e05e98ec84aee56ea2; xq_r_token.sig=PsJbVE-f5UrXmAWhJFGj1bmNQNs; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=1733473480; u.sig=2sMTnVmBVOASyCZs6lbVBQ6Zfgs; Hm_lvt_1db88642e346389874251b5a1eded6e3=1513578346,1513663485,1514177432,1514389832; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1514389994',
                   'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Referer': 'https://xueqiu.com/P/ZH010389'}
        # url='https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH010389&count=20&page={}'.format(page)
        r = requests.get(url=url, headers=headers)
        print r.status_code
        if r.status_code != 200:
            print 'failed to get web content'
            return None
        else:
            return r.text


def main():
    # gethisotry(2)


if __name__ == '__main__':
    main()
