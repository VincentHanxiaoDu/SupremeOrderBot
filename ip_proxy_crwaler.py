import requests
from lxml import etree

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.339h'}

def get_proxy_info(url):
    req = requests.get(url, headers=UA).text
    document = etree.HTML(req)
    table = document.xpath('//tbody')[0]
    all = table.xpath('tr')
    result = {}
    for i in all:
        all_info = i.xpath('td')
        ip = all_info[0].xpath('text()')[0]
        info = {
            'port': all_info[1].xpath('text()')[0],
            'code': all_info[2].xpath('text()')[0],
            'country': all_info[3].xpath('text()')[0],
            'anonymity': all_info[4].xpath('text()')[0],
            'google': all_info[5].xpath('text()')[0],
            'https': all_info[6].xpath('text()')[0],
            'last_check': all_info[7].xpath('text()')[0]
        }
        result[ip] = info
    return result

def crawl_all():
    result = {}
    all_url = ['https://www.us-proxy.org/', 'https://free-proxy-list.net/']
    for i in all_url:
        result.update(get_proxy_info(i))
    return result

# print(get_proxy_info('https://www.us-proxy.org/'))