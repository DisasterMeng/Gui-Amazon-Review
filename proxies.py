import random
import requests
import threading

from lxml import etree
from queue import Queue
from threading import Timer
from fake_useragent import UserAgent
from multiprocessing import cpu_count
from datetime import datetime, timedelta

from utils import request_message, getAmazonDomain, is_robot, wait, amazon_headers

MAX_PROXY_REQUESTS_NUM = 2

SCANNING_TIME = 0

MAX_PROXY_POOL_NUM = {
    'AE': 0,
    'CN': 0,
    'JP': 0,
    'US': 0,
    'UK': 0,
    'FR': 0,
    'DE': 0,
    'ES': 0,
    'IT': 0,
    'CA': 0,
    'IN': 0,
    'AU': 0,
    'GB': 0,
    'MX': 0,
    'BR': 0
    # 'SG': 'https://www.amazon.com.sg'
}

proxy_url = 'http://http.tiqu.alicdns.com/getip3?num={num}&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0' \
            '&lb=1&sb=0&pb=4&mr=2&regions=&gm=4'

proxies_mate = 'https://{host}:{port}'


class Proxy:
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with Proxy._instance_lock:
                if not hasattr(cls, '_instance'):
                    Proxy._instance = super().__new__(cls)
        return Proxy._instance

    def __init__(self):
        self.agents = {}
        self.proxies_num = 0
        self.add_agent()
        timer(self)

    def agent_pool(self, country=None, proxy_num=1):
        proxies_array = []
        print('开始请求代理')
        session, response = self.request(requests.session(), proxy_url
                                         .format(num=min(proxy_num, cpu_count()) if country else 1), types='json')
        if 'success' in response and response['success']:
            print('请求代理成功')
            self.proxies_num = 0
            for item in response['data']:
                proxies = {
                    'http': proxies_mate.format(host=item['ip'], port=item['port']),
                    'https': proxies_mate.format(host=item['ip'], port=item['port']),
                }
                proxies_array.append({'session': session, 'proxies': proxies, 'expire_time': item['expire_time']})
            if country:
                print('有国家参数, 进行amazon访问处理，判断ip是否有效')
                proxies_data = {}
                thread_list = []
                q = Queue()
                for proxies_item in proxies_array:
                    t = threading.Thread(target=self.amazon_robot_check, args=(proxies_item, country, q))
                    t.setDaemon(True)
                    thread_list.append(t)
                    t.start()

                for thread_item in thread_list:
                    thread_item.join()
                    results = q.get()
                    if results:
                        if country in proxies_data:
                            proxies_data[country].append(results)
                        else:
                            proxies_data[country] = [results]

                print('获取有效代理对象: ', proxies_data if proxies_data else None)
                return proxies_data if proxies_data else None
            else:
                print('无国家参数, 不需要处理, 直接返回代理')
                return proxies_array.pop()
        else:
            self.proxies_num += 1
            print('请求代理失败, 正在重试...重试次数为: ', self.proxies_num)
            if self.proxies_num < MAX_PROXY_REQUESTS_NUM:
                wait()
                return self.agent_pool(country, proxy_num)
            else:
                print('请求代理失败, 重试已达最大次数')
                return response

    def amazon_robot_check(self, data, country, q):
        print('正在进行amazon机器人验证')
        try:
            cur_header = amazon_headers.copy()
            cur_header['user-agent'] = UserAgent().random
            session, response = self.request(data['session'], getAmazonDomain(country), headers=cur_header,
                                             proxies=data['proxies'])
            if not is_robot(etree.HTML(response)):
                data['session'] = session
                q.put(data)
            else:
                print('机器人验证')
                q.put(None)
        except Exception as e:
            print(e)
            q.put(None)

    def add_agent(self):
        # add_agent_arr 需要添加代理的国家
        add_agent_arr = []
        print('检测代理是否需要添加')
        for item in MAX_PROXY_POOL_NUM:
            if MAX_PROXY_POOL_NUM[item] == 0:
                continue
            cur_proxy_num = len(self.agents[item]) if item in self.agents else 0
            if cur_proxy_num >= MAX_PROXY_POOL_NUM[item]:
                continue
            add_agent_arr.append({'country': item, 'proxy_num': (MAX_PROXY_POOL_NUM[item] - cur_proxy_num)})
        if add_agent_arr:
            print('代理需要添加的国家有: ', ','.join([item['country'] for item in add_agent_arr]))
            for item in add_agent_arr:
                results = self.agent_pool(item['country'], item['proxy_num'])
                if results:
                    if item['country'] in self.agents:
                        self.agents[item['country']].extend(results[item['country']])
                    else:
                        self.agents[item['country']] = results[item['country']]
                else:
                    continue
            wait()
            self.add_agent()
        else:
            print('代理以达到设定数量, 不在进行添加')
            return None

    def remove_expired(self):
        print('正在移除过期代理')
        for country in self.agents:
            for index, item in enumerate(self.agents[country]):
                if self.compare_time(item['expire_time']):
                    print('存在过期代理进行移除')
                    self.agents[country].pop(index)
                    self.add_agent()

    def get_proxies(self, country=None):
        if country:
            if country in self.agents:
                index = random.randint(0, len(self.agents[country]) - 1)
                agent = self.agents[country][index]
                if self.compare_time(agent['expire_time']):
                    print('取出当前代理发现过期')
                    self.agents[country].pop(index)
                    self.add_agent()
                    return self.get_proxies(country)
                return agent['session'], agent['proxies']
            else:
                results = self.agent_pool(country, proxy_num=1)
                if results:
                    agent = random.choice(results[country])
                    return agent['session'], agent['proxies']
                wait()
                return self.get_proxies(country)
        else:
            return self.agent_pool()

    @staticmethod
    def request(session, url, headers=None, proxies=None, types='txt'):
        response = session.get(url, headers=headers, proxies=proxies, timeout=20)
        response.encoding = 'utf-8'
        return session, request_message(response, types)

    @staticmethod
    def compare_time(date):
        # 2020-04-14 11:44:46
        now = (datetime.now() + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
        return datetime.strptime(now, '%Y-%m-%d %H:%M:%S') > datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


# 定时器
def timer(proxy):
    # 移除过期代理
    if SCANNING_TIME == 0:
        return None
    proxy.remove_expired()
    t = Timer(SCANNING_TIME, timer, (proxy,))
    t.start()
