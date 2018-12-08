#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt

from guoren_api import GuorenApi
from tonghuashui_api import TonghuashuiApi
from xueqiu_data import XueqiuStockList
from xueqiu_strategy import XueqiuStrategies

plt.style.use('ggplot')


def generate_data_by_code_using_guoren(code, name, reserved_count=1800, root_dir='gen/custom/'):
    os.makedirs(root_dir, exist_ok=True)
    plt.figure(num=1, figsize=(8, 36))
    plt.clf()
    guoren_api = GuorenApi(code)

    plt.subplot(10, 1, 1)
    plt.title('历史PE')
    guoren_content = guoren_api.submit_req_pe()
    print(guoren_content)
    pe_series = GuorenApi.parse_json_to_series_filter_dirty(guoren_content, lambda x: (x[0], float(x[1])),
                                                            reserved_count=reserved_count)
    total_len = len(pe_series)
    if total_len > 0:
        pe = pe_series.get(total_len - 1)
        gt_now_pe_percent = len(pe_series[pe_series > pe]) / total_len * 100
        pe = round(pe, 2)
        pe_series.plot()

    plt.subplot(10, 1, 2)
    plt.title('历史PB')
    guoren_content = guoren_api.submit_req_pb()
    print(guoren_content)
    pb_series = GuorenApi.parse_json_to_series(guoren_content, reserved_count=reserved_count)
    total_len = len(pb_series)
    if total_len > 0:
        pb = pb_series.get(total_len - 1)
        gt_now_pb_percent = len(pb_series[pb_series > pb]) / total_len * 100
        pb = round(pb, 2)
        pb_series.plot()

    plt.subplot(10, 1, 3)
    plt.title('5日均成交量(单位:10万)')
    guoren_content = guoren_api.submit_req_volume()
    print(guoren_content)
    try:
        volume_series = GuorenApi.parse_json_to_series_filter_dirty(guoren_content,
                                                                    lambda x: (x[0], int(x[1] / 100000)),
                                                                    reserved_count=reserved_count)
        total_len = len(volume_series)
        if total_len > 0:
            gt_now_volume_percent = len(
                volume_series[volume_series > volume_series.get(len(volume_series) - 1)]) / total_len * 100
            volume_series.plot()
    except TypeError:
        volume_series = None
        gt_now_volume_percent = None
        print("error to print")

    plt.subplot(10, 1, 4)
    plt.title('ROE')
    guoren_content = guoren_api.submit_req_roe()
    print(guoren_content)
    GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

    plt.subplot(10, 1, 5)
    plt.title('股息率')
    guoren_content = guoren_api.submit_req_dy()
    print(guoren_content)
    dy_series = GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count)
    dy = round(dy_series.get(len(dy_series) - 1), 2)
    dy_series.plot()

    plt.subplot(10, 1, 6)
    plt.title('收入增长率')
    guoren_content = guoren_api.submit_req_income_grow()
    print(guoren_content)
    GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

    plt.subplot(10, 1, 7)
    plt.title('利润增长率')
    guoren_content = guoren_api.submit_req_profie_grow()
    print(guoren_content)
    GuorenApi.parse_json_to_series_filter_dirty(guoren_content, lambda x: (x[0], int(x[1] * 100)),
                                                reserved_count=reserved_count).plot()

    tonghuashui_api = TonghuashuiApi(code)
    tonghuashui_api.submit_req()
    if tonghuashui_api.is_bank_data():
        plt.subplot(10, 1, 8)
        plt.title('拨备覆盖率')
        tonghuashui_api.get_bank_provision_coverage_series(int(pe_series.first_valid_index()[0:2])).plot()

        plt.subplot(10, 1, 9)
        plt.title('不良贷款率')
        tonghuashui_api.get_bank_bad_debts_series(int(pe_series.first_valid_index()[0:2])).plot()

        plt.subplot(10, 1, 10)
        plt.title('净息差')
        tonghuashui_api.get_bank_interest_series(int(pe_series.first_valid_index()[0:2])).plot()
    else:
        plt.subplot(10, 1, 8)
        plt.title('毛利率')
        guoren_content = guoren_api.submit_req_gross()
        print(guoren_content)
        GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

        plt.subplot(10, 1, 9)
        plt.title('净利率')
        guoren_content = guoren_api.submit_req_interest()
        print(guoren_content)
        GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

        plt.subplot(10, 1, 10)
        plt.title('总资产周转率')
        guoren_content = guoren_api.submit_req_turnover()
        print(guoren_content)
        GuorenApi.parse_json_to_series(guoren_content, lambda x: x * 100, reserved_count=reserved_count).plot()

    title = '{} {}\n动态市盈率:{}, 市净率:{},股息率:{}\n'.format(
        name, code, pe, pb, dy)
    title += '\n{} 到 {} {}%时间大于当前市盈率\n'.format(pe_series.first_valid_index(), pe_series.last_valid_index(),
                                               round(gt_now_pe_percent, 2))
    title += '\n{} 到 {} {}%时间大于当前市净率\n'.format(pb_series.first_valid_index(), pb_series.last_valid_index(),
                                               round(gt_now_pb_percent, 2))
    if volume_series is not None and gt_now_volume_percent is not None:
        title += '\n{} 到 {} {}%时间大于当前成交量\n'.format(volume_series.first_valid_index(), volume_series.last_valid_index(),
                                                   round(gt_now_volume_percent, 2))
    if tonghuashui_api.is_bank_data():
        max_provision = tonghuashui_api.get_bank_max_provision_coverage(int(pe_series.first_valid_index()[0:2]))
        max_bad = tonghuashui_api.get_bank_max_bad_debts(int(pe_series.first_valid_index()[0:2]))
        max_interest = tonghuashui_api.get_bank_max_interest(int(pe_series.first_valid_index()[0:2]))
        if max_provision[0] == max_bad[0]:
            title += '\n截止{} 拨备覆盖率: {}, 不良率: {}\n'.format(max_provision[0], max_provision[1], max_bad[1])
        else:
            title += '\n{} 拨备覆盖率: {}, {} 不良率: {}\n'.format(max_provision[0], max_provision[1], max_bad[0], max_bad[1])
        title += '\n截止{} 净息差: {}\n'.format(max_interest[0], max_interest[1])
    plt.suptitle(title)
    plt.savefig(root_dir + '{}_{}.png'.format(name, code))


def generate_data_from_guoren_by_xueqiu_strategy(xueqiu, is_just_data=False):
    # step 1: req filter strategy from xueqiu
    content = xueqiu.submit_req()
    print(content)
    xueqiu_stock_list = XueqiuStockList.create(content)
    while xueqiu_stock_list.has_more():
        content = xueqiu.submit_req(xueqiu_stock_list.get_req_new_page())
        print(content)
        xueqiu_stock_new_page_list = XueqiuStockList.create(content)
        xueqiu_stock_list.append_list(xueqiu_stock_new_page_list.stock_list)
    print("\ncount:{}".format(len(xueqiu_stock_list.stock_list)))

    os.makedirs('gen/{}/'.format(xueqiu.name), exist_ok=True)
    file = open('gen/{}.txt'.format(xueqiu.name), 'w', encoding='utf-8')
    file.write('{}'.format(xueqiu_stock_list.stock_list))
    file.close()
    if not is_just_data:
        # step 2: draw pic totally from guoren
        for idx, stock_item in enumerate(xueqiu_stock_list.stock_list):
            generate_data_by_code_using_guoren(stock_item.symbol[2:], stock_item.name,
                                               root_dir='gen/{}/'.format(xueqiu.name))


def generate_data_by_xueqiu_strategy(xueqiu):
    # step 1: req filter strategy from xueqiu
    content = xueqiu.submit_req()
    print(content)
    xueqiu_stock_list = XueqiuStockList.create(content)
    while xueqiu_stock_list.has_more():
        content = xueqiu.submit_req(xueqiu_stock_list.get_req_new_page())
        print(content)
        xueqiu_stock_new_page_list = XueqiuStockList.create(content)
        xueqiu_stock_list.append_list(xueqiu_stock_new_page_list.stock_list)
    print("\ncount:{}".format(len(xueqiu_stock_list.stock_list)))

    os.makedirs('gen/{}/'.format(xueqiu.name), exist_ok=True)
    file = open('gen/{}.txt'.format(xueqiu.name), 'w', encoding='utf-8')
    file.write('{}'.format(xueqiu_stock_list.stock_list))
    file.close()

    # step 2: draw pic and req detail from guoren
    for idx, stock_item in enumerate(xueqiu_stock_list.stock_list):
        plt.figure(num=1, figsize=(8, 30))
        plt.clf()
        plt.suptitle('{} {}\n动态市盈率:{}, 市净率:{},股息率:{}'.format(
            stock_item.name, stock_item.symbol, stock_item.pettm, stock_item.pb, stock_item.dy))
        print('symbol:' + stock_item.symbol[2:])
        guoren_api = GuorenApi(stock_item.symbol[2:])

        plt.subplot(811)
        plt.title('历史PE')
        guoren_content = guoren_api.submit_req_pe()
        print(guoren_content)
        GuorenApi.parse_json_to_series(guoren_content).plot()

        plt.subplot(812)
        plt.title('历史PB')
        guoren_content = guoren_api.submit_req_pb()
        print(guoren_content)
        GuorenApi.parse_json_to_series(guoren_content).plot()

        plt.subplot(813)
        plt.title('5日均成交量(单位:10万)')
        guoren_content = guoren_api.submit_req_volume()
        print(guoren_content)
        try:
            GuorenApi.parse_json_to_series_filter_dirty(guoren_content, lambda x: (x[0], int(x[1] / 100000))).plot()
        except TypeError:
            print("error to print")

        plt.subplot(814)
        plt.title(stock_item.roediluted.name)
        stock_item.roediluted.sort_index(ascending=True).plot()
        plt.subplot(815)
        plt.title(stock_item.income_grow.name)
        stock_item.income_grow.sort_index(ascending=True).plot()
        plt.subplot(816)
        plt.title(stock_item.profit_grow.name)
        stock_item.profit_grow.sort_index(ascending=True).plot()
        plt.subplot(817)
        plt.title(stock_item.gross.name)
        stock_item.gross.sort_index(ascending=True).plot()
        plt.subplot(818)
        plt.title(stock_item.interest.name)
        stock_item.interest.sort_index(ascending=True).plot()
        # plt.show()
        plt.savefig('gen/{}/{}_{}.png'.format(xueqiu.name, stock_item.name, stock_item.symbol[2:]))


# generate_data_from_guoren_by_xueqiu_strategy(XueqiuStrategies.stable_strict(), True)
# generate_data_from_guoren_by_xueqiu_strategy(XueqiuStrategies.stable_short(), True)
# generate_data_from_guoren_by_xueqiu_strategy(XueqiuStrategies.stable(), True)
# generate_data_from_guoren_by_xueqiu_strategy(XueqiuStrategies.fastest(), True)
# generate_data_from_guoren_by_xueqiu_strategy(XueqiuStrategies.faster(), True)
# generate_data_from_guoren_by_xueqiu_strategy(XueqiuStrategies.fast(), True)

# generate_data_by_code_using_guoren('601668', '中国建筑', 1600)
# generate_data_by_code_using_guoren('000732', '泰禾集团', 1600)
# generate_data_by_code_using_guoren('600048', '保利地产', 1600)
# generate_data_by_code_using_guoren('000002', '万科A', 1600)
# generate_data_by_code_using_guoren('600383', '金地集团', 1600)
# generate_data_by_code_using_guoren('000671', '阳光城', 1600)

# generate_data_by_code_using_guoren('600066', '宇通客车', 1400)
# generate_data_by_code_using_guoren('000625', '长安汽车', 1400)
# generate_data_by_code_using_guoren('600104', '上汽集团', 1400)

# generate_data_by_code_using_guoren('000651', '格力电器', 1400)
# generate_data_by_code_using_guoren('000333', '美的集团', 1400)

# generate_data_by_code_using_guoren('601318', '中国平安', 1400)
# generate_data_by_code_using_guoren('002415', '海康威视', 1400)

# generate_data_by_code_using_guoren('002304', '洋河股份', 1400)
# generate_data_by_code_using_guoren('600887', '伊利股份', 1400)

# generate_data_by_code_using_guoren('600886', '国投电力', 1400)
# generate_data_by_code_using_guoren('600674', '川投能源', 1400)

generate_data_by_code_using_guoren('601166', '兴业银行', 1800)
# generate_data_by_code_using_guoren('601939', '建设银行', 1800)
# generate_data_by_code_using_guoren('600000', '浦发银行', 1800)
# generate_data_by_code_using_guoren('601009', '南京银行', 1800)
# generate_data_by_code_using_guoren('600016', '民生银行', 1800)
# generate_data_by_code_using_guoren('600036', '招商银行', 1800)
# generate_data_by_code_using_guoren('000001', '平安银行', 1600)

# generate_data_by_code_using_guoren('600741', '华域汽车', 1600)

