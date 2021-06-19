import requests
import threading
from lxml import etree
from ip_proxy_crwaler import get_proxy_info
import re
import random

def start_threads(threads, daemon=True):
    for i in threads:
        i.setDaemon(daemon)
        i.start()
    for i in threads:
        i.join()

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.339h'}

def crawl_supreme_all_goods():
    url = 'http://www.supremenewyork.com/shop/all'
    req = requests.get(url, headers=UA).text
    document = etree.HTML(req)
    return document.xpath('//div[@id="container"]/article/div/a')

def get_current_goods_info(display_sold_out=True):
    '''Returns all current goods' info in a dict in form of {{name+'["color"]': {'url': good_url, 'img': img}}, ...}'''
    def get_info(each):
        good_url = 'https://www.supremenewyork.com{}'.format(each.xpath('@href')[0])
        img = each.xpath('img/@src')[0]
        good_req = requests.get(good_url, headers=UA).text
        name = re.findall('itemprop="name">(.*?)</h1>', good_req, re.S)[0]
        color = re.findall('itemprop="model">(.*?)</p>', good_req, re.S)[0]
        goods.update(
            {name+'["{}"]'.format(color): {'url': good_url, 'img': img}}
        )
    goods = {}
    all = crawl_supreme_all_goods()
    threads = []
    for good in all:
        if display_sold_out or not good.xpath('div'):
            thread = threading.Thread(target=get_info, args=(good,))
            threads.append(thread)
    start_threads(threads)
    return goods

def get_current_goods_available_list():
    '''Returns a set contains all available goods'''
    def get_name(each):
        good_url = 'https://www.supremenewyork.com{}'.format(each.xpath('@href')[0])
        good_req = requests.get(good_url, headers=UA).text
        name = re.findall('itemprop="name">(.*?)</h1>', good_req, re.S)[0]
        color = re.findall('itemprop="model">(.*?)</p>', good_req, re.S)[0]
        goods.add(name+'["{}"]'.format(color))
    goods = set()
    all = crawl_supreme_all_goods()
    threads = []
    for good in all:
        if not good.xpath('div'):
            thread = threading.Thread(target=get_name, args=(good,))
            threads.append(thread)
    start_threads(threads)
    return goods

def get_goods_droplists():
    proxies = get_proxy_info('https://www.us-proxy.org/')
    proxies_choices = {}
    for k, v in proxies.items():
        if v['https'] == 'yes':
            proxies_choices[k] = v
    def get_each(sub_url):
        def get_info(each):
            name = each.xpath('@data-itemname')[0]
            itemid = each.xpath('@data-itemid')[0]
            info_url = 'https://www.supremecommunity.com/season/itemdetails/{}/'.format(itemid)
            proxy_ok = False
            try_time = 0
            choices = list(proxies_choices)
            color_str = ''
            while not proxy_ok and try_time < 10:
                choice = random.choice(choices)
                proxy = 'http://' + choice + ':' + proxies[choice]['port']
                try:
                    info_req = requests.get(info_url, headers=UA, proxies={'http': proxy, 'https': proxy}).text
                    try:
                        color_str = re.findall('Colorways: <span>(.*?)</span>', info_req)[0]
                    except:
                        pass
                    proxy_ok = True
                except:
                    try:
                        proxies_choices.pop(choice)
                    except:
                        pass
                    proxy_ok = False
                    try_time += 1
            if not proxy_ok:
                info_req = requests.get(info_url, headers=UA).text
                try:
                    color_str = re.findall('Colorways: <span>(.*?)</span>', info_req)[0]
                except:
                    pass
            week_info[name] = color_str
            print(name, itemid, color_str)
        week_url = 'https://www.supremecommunity.com' + sub_url
        week_req = requests.get(week_url, headers=UA).text
        document = etree.HTML(week_req)
        week_all_goods = document.xpath(
            '//div[@class="masonry__container masonry--active"]/div/div/div[@class="card-details"]')
        week_info = {}
        threads = []
        for i in week_all_goods:
            thread = threading.Thread(target=get_info, args=(i,))
            threads.append(thread)
        start_threads(threads)
        print(sub_url.split('/')[-2])
        result = {sub_url.split('/')[-2]: week_info}
        return result
    info = {}
    url = 'https://www.supremecommunity.com/season/latest/droplists/'
    req = requests.get(url, headers=UA).text
    weeks = re.findall('<a href="(.*?)" class="block">', req)
    weeks = list(set(weeks))
    for week in weeks:
        info.update(get_each(week))
    return info

if __name__ == "__main__":
    print(get_goods_droplists())
