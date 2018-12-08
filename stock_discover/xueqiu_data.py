import json
from json.decoder import WHITESPACE

from pandas import Series


class StockDecoder(json.JSONDecoder):
    def decode(self, s, _w=WHITESPACE.match):
        dict_data = super().decode(s)
        if dict_data['count'] > 0:
            local_stock_data = XueqiuStockList(total_count=dict_data['count'])
            for item in dict_data['list']:
                stock = XueqiuStock.create(item)
                local_stock_data.append(stock)
            return local_stock_data
        return XueqiuStockList()


class XueqiuStockList(object):
    def __init__(self, stock_list=None, total_count=0):
        if stock_list is None:
            stock_list = []
        self.stock_list = stock_list
        self.total_count = total_count
        self.page_count = 30

    def append(self, item):
        self.stock_list.append(item)

    def append_list(self, append_list):
        self.stock_list.extend(append_list)

    def has_more(self):
        return self.total_count > len(self.stock_list)

    def get_req_new_page(self):
        return len(self.stock_list) / self.page_count + 1

    @staticmethod
    def create(json_content):
        return json.loads(json_content, cls=StockDecoder)


class XueqiuStock(object):
    def __init__(self, name='', symbol='', pettm=0, pb=0, dy=0, roediluted=None, income_grow=None,
                 profit_grow=None, gross=None, interest=None):
        self.name = name
        self.symbol = symbol
        self.pettm = pettm
        self.pb = pb
        self.dy = dy
        self.roediluted = roediluted
        self.income_grow = income_grow
        self.profit_grow = profit_grow
        self.gross = gross
        self.interest = interest
        self.pct_rate_1y = None

    def __repr__(self):
        output = '\n=============={0} ({1})==============\n 动态市盈率: {2} \n'.format(self.name, self.symbol, self.pettm)
        if self.pct_rate_1y is not None:
            output += ' 近一年涨跌幅: {0}% \n'.format(self.pct_rate_1y)
        output += '\n------{}------\n{}'.format(self.roediluted.name, self.roediluted)
        output += '\n------{}------\n{}'.format(self.income_grow.name, self.income_grow)
        output += '\n------{}------\n{}'.format(self.profit_grow.name, self.profit_grow)
        output += '\n------{}------\n{}'.format(self.gross.name, self.gross)
        output += '\n------{}------\n{}\n'.format(self.interest.name, self.interest)
        return output

    @classmethod
    def create(cls, item):
        stock = cls()
        stock.name = item['name']
        stock.symbol = item['symbol']
        stock.pettm = item['pettm']
        stock.pct_rate_1y = item['pct1y']
        stock.pb = item['pb']
        stock.dy = item['dy']
        stock.roediluted = Series(item['roediluted']).sort_index(ascending=False)
        stock.roediluted.name = 'ROE'
        stock.income_grow = Series(item['mbig']).sort_index(ascending=False)
        stock.income_grow.name = '收入增长率'
        stock.profit_grow = Series(item['nig']).sort_index(ascending=False)
        stock.profit_grow.name = '利润增长率'
        stock.gross = Series(item['sgpr']).sort_index(ascending=False)
        stock.gross.name = '毛利率'
        stock.interest = Series(item['snpr']).sort_index(ascending=False)
        stock.interest.name = '净利率'
        return stock
