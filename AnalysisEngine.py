from DbUtilities.MariaHelper import MariaHelper
import requests
import random
from lxml import etree
import re
import pandas as pd
import math
import json
import threading
import time
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

fund_dict = {}
fund_list = []
fund_lsjz_list = []

mutex = threading.Lock()


class AnalysisEngine(object):
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
        self.header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                       'Accept-Encoding': 'gzip, deflate, sdch',
                       'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Connection': 'keep-alive',
                       'User-Agent': random.choice(self.user_agents)}
        self.proxies = ['http://118.178.124.33:3128', 'http://139.129.166.68:3128',
                        'http://61.163.39.70:9999', 'http://61.143.228.162']
        self.html = ''

        self.fundCode = '000001'
        self.pageIndex = 1
        self.pageSize = 500
        self.lsjzHeader = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ru;q=0.6',
            'Connection': 'keep-alive',
            'Cookie': 'qgqp_b_id=41c434be00dacbd13bca2d0f831d44ca; st_pvi=02911440853997; st_sp=2019-04-11%2023%3A18%3A14; st_inirUrl=; st_si=59935242760746; st_sn=1; st_psi=20190411231813797-0-1868636963; st_asi=delete',
            'Host': 'api.fund.eastmoney.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.99 YaBrowser/19.1.1.909 Yowser/2.5 Safari/537.36',
            'Referer': 'http://fundf10.eastmoney.com/jjjz_%s.html' % self.fundCode
        }
        self.lsjzParam = {
            'callback': 'jQuery18307293101866392497_1551105476194',
            'pageSize': self.pageSize,
            'fundCode': self.fundCode,
            'pageIndex': self.pageIndex,
        }
        self.lsjzUrl = 'http://api.fund.eastmoney.com/f10/lsjz'
        self.lsjzThreadCount = 4
        self.lsjzDF = pd.DataFrame()
        # self.lsjzDF = pd.DataFrame(columns=('fundCode', 'FSRQ', 'DWJZ', 'LJJZ', 'SDATE', 'ACTUALSYI', 'NAVTYPE', 'JZZZL', 'SGZT', 'SHZT', 'FHFCZ', 'FHFCBZ', 'DTYPE', 'FHSP'))
        self.mutex = threading.Lock()

    def getContentByParsingUrl(self, url, charset='gbk'):
        if url is None:
            return None

        try:
            html = requests.get(url, headers=self.header  # , proxies={'http': random.choice(self.proxies)}
                                ).content.decode(charset)

        except Exception as e:
            print("Open url failed, error: {}".format(e))
            return None

        self.html = html

    def getFundLsjzByParsingUrl(self):
        mh = MariaHelper()
        results = mh.queryByTableName('t_funds')
        if results == None:
            pass

        resultCount = len(results)
        for i in range(self.lsjzThreadCount):
            for row in results[int(resultCount * i/self.lsjzThreadCount): int(resultCount * (i+1)/self.lsjzThreadCount)]:
                self.fundCode = row['codeno']
                self.lsjzHeader['Referer'] = 'http://fundf10.eastmoney.com/jjjz_%s.html' % self.fundCode
                self.lsjzParam['fundCode'] = self.fundCode
                lsjzJson = requests.get(
                    self.lsjzUrl, headers=self.lsjzHeader, params=self.lsjzParam)
                tt = re.findall(r'\((.*?)\)', lsjzJson.text)[0]  # 提取dict
                lsjzList = json.loads(tt)['Data']['LSJZList']  # 获取历史净值数据
                totalCount = json.loads(tt)['TotalCount']
                lsjzDF = pd.DataFrame(lsjzList)
                lsjzDF['fundCode'] = self.fundCode

    def saveFundLsjzByCodeno(self, codeno):
        mh = MariaHelper()
        result = mh.queryByCodeno('t_funds', codeno)
        if result == None:
            pass

        # result的格式为: [{'codeno': '000001', 'name': '华夏成长', 'url': 'http://fund.eastmoney.com/000001.html'}]
        self.fundCode = result[0]['codeno']
        self.lsjzHeader['Referer'] = 'http://fundf10.eastmoney.com/jjjz_%s.html' % self.fundCode
        self.lsjzParam['fundCode'] = self.fundCode
        lsjzJson = requests.get(
            self.lsjzUrl, headers=self.lsjzHeader, params=self.lsjzParam)
        tt = re.findall(r'\((.*?)\)', lsjzJson.text)[0]
        totalCount = json.loads(tt)['TotalCount']
        print("====================== totalCount: %s ======================" % totalCount)
        nLoopTimes = math.ceil(totalCount / self.pageSize)
        print("====================== nLoopTimes: %s ======================" % nLoopTimes)
        i = 1
        lsjzThread_list = []
        while i <= nLoopTimes:
            t = threading.Thread(
                target=self.extractFundsLsjzDetail, args=(self.fundCode, i))
            lsjzThread_list.append(t)
            t.start()
            i += 1

        for th in lsjzThread_list:
            th.join()

        mh.saveToTable('t_funds_lsjz', fund_lsjz_list)
        mh.close()

    def extractFundsLsjzDetail(self, fundCode, pageIndex):
        self.mutex.acquire()

        self.lsjzHeader['Referer'] = 'http://fundf10.eastmoney.com/jjjz_%s.html' % fundCode
        self.lsjzParam['fundCode'] = fundCode
        self.lsjzParam['pageIndex'] = pageIndex
        lsjzJson = requests.get(
            self.lsjzUrl, headers=self.lsjzHeader, params=self.lsjzParam)
        tt = re.findall(r'\((.*?)\)', lsjzJson.text)[0]
        lsjzList = json.loads(tt)['Data']['LSJZList']  # 获取历史净值数据
        lsjzDF = pd.DataFrame(lsjzList)
        lsjzDF.insert(0, 'fundCode', self.fundCode)
        fund_lsjz_list.extend(lsjzDF.values.tolist())

        self.mutex.release()

    def extractFundsDetail(self):
        if self.html is None:
            return None

        try:
            html = etree.HTML(self.html)
            code_content_list = html.xpath('//div[@id="code_content"]/div')
            thread_list = []
            thread_count = len(code_content_list)  # len(code_content_list)
            for i in range(thread_count):
                t = threading.Thread(
                    target=shapeFundsCatalogue, args=(code_content_list[i],))
                thread_list.append(t)
                t.start()

            for th in thread_list:
                # t.setDaemon(True)
                th.join()
            mh = MariaHelper()
            mh.saveToTable('t_funds', fund_list)
            # mh.queryByTableName('t_funds')
            mh.close()
        except Exception as e:
            print("extractFundsDetail()函数异常", e)


def shapeFundsCatalogue(arg):
    mutex.acquire()
    num_box = arg
    li_list = num_box.xpath('./ul[@class="num_right"]//li')
    for li in li_list:
        if len(li) > 0:
            fund_codeno_name_list = li.xpath('./div/a/text()')
            fund_profile_url = li.xpath('./div/a[1]/@href')
            fund_profile_url = "".join(fund_profile_url)

            fund_codeno_name = fund_codeno_name_list[0]
            # fund_codeno
            fund_codeno = re.findall(
                r"（(.+)）", fund_codeno_name)
            fund_codeno = "".join(fund_codeno)
            # fund_name
            fund_name = fund_codeno_name.split('）')[1]
            # print("{0} {1} {2}".format(fund_codeno, fund_name, fund_profile_url))
            temp_list = []
            temp_list.append(fund_codeno)
            temp_list.append(fund_name)
            temp_list.append(fund_profile_url)
            fund_list.append(temp_list)
    mutex.release()
