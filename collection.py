# config=utf-8
# Author Gscsd5


from bs4 import BeautifulSoup
import requests
from random import randint
from urllib.parse import quote


class Collection:
    def __init__(self, conf_info):
        self.title = quote(conf_info['title'])
        self.country = conf_info['country']
        self.cookie = conf_info['cookie']
        self.url_list = []
        self.url = 'https://www.shodan.io/search?query=title%3A%22{}%22+country%3A%22{}%22'.format(self.title, self.country)
        self.ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64;'
            ' Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729;'
            ' .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; KB974488)',
            'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36 PTST/190509.230546 PTST/200319.140320',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 PTST/200319.140320',
        ]
        self.header = {
            'Host': 'www.shodan.io',
            'Connection': 'close',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.ua[randint(0, 4)],
            'Sec-Fetch-Dest': 'document',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                      'q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'Cookie': self.cookie
        }

    def start_col(self):
        print('开始采集URL……')
        num = 1
        while num < 21:
            page = '&page={}'.format(num)
            request_url = self.url + page
            print('正在采集第{}页'.format(num))
            content = requests.get(url=request_url, headers=self.header)
            info = BeautifulSoup(content.content, 'html.parser')
            tet = info.find_all('div')[9]('a')
            for k in tet:
                if k['href'] == 'https://monitor.shodan.io':
                    continue
                elif '//' in k['href']:
                    # self.url_list.append(k['href'])
                    if num == 1:
                        with open('url.txt', 'w') as f:
                            f.write(k['href'] + '\n')
                            f.close()
                    else:
                        with open('url.txt', 'a') as f:
                            f.write(k['href'] + '\n')
                            f.close()

            next_next = info.find_all('li')[-1]
            if 'Next' in next_next.text:
                num += 1
        print('采集完成')

    def deal(self):
        print('正在处理URL地址……')
        with open('url.txt', 'r') as f:
            for u in f:
                if u not in self.url_list:
                    self.url_list.append(u)
            f.close()
        with open('url.txt', 'w') as q:
            for k in self.url_list:
                q.write(k)
            q.close()
        print('URL处理结束')


if __name__ == '__main__':
    with open('conf.con', encoding='utf-8') as f:
        conf_info = eval(f.read())
    cms_col = Collection(conf_info)
    cms_col.start_col()
    cms_col.deal()





























