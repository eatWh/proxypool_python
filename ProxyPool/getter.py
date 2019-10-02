import datetime
import re
from lxml import etree
from ProxyPool.requester import get_html
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Proxymetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=Proxymetaclass):

    def get_raw_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_free(self):
        for i in range(1, 4):
            url = "http://ip.jiangxianli.com/?page={}".format(i)
            rep = get_html(url)
            if rep is not None:
                results = re.compile(r'<tr>\s*<td>\d+</td>\s*<td>([\d\.]+)</td>\s*<td>(\d+)<').findall(rep)
                if results:
                    for result in results:
                        ip_port = result[0] + ":" + result[1]
                        yield ip_port
                        time.sleep(0.5)

    def crawl_quanwang(self):
        proxies = []
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('http://www.goubanjia.com')
        tr_list = driver.find_elements_by_xpath('//*[@id="services"]/div/div[2]/div/div/div/table/tbody/tr')
        for tr in tr_list:
            ip_port = tr.text.split(" ")[0]
            proxies.append(ip_port)
        driver.close()
        return proxies

    def crawl_yundaili(self):
        for i in range(1, 4):
            url = "http://www.ip3366.net/free/?page={}".format(i)
            rep = get_html(url)
            if rep is not None:
                html = etree.HTML(rep)
                tr_list = html.xpath('//*[@id="list"]/table/tbody/tr')
                for tr in tr_list:
                    ip = tr.xpath('./td[1]/text()')
                    port = tr.xpath('./td[2]/text()')
                    date = tr.xpath('./td[last()]/text()')
                    if ip and port and date:
                        date = datetime.datetime.strptime(date[0].split(" ")[0], '%Y/%m/%d').date()
                        today = datetime.datetime.now().date()
                        if date == today:
                            ip_port = ip[0] + ":" + port[0]
                            yield ip_port.replace(' ', '')
                            time.sleep(0.5)

    def crawl_89ip(self):
        for i in range(1, 4):
            url = "http://www.89ip.cn/index_{}.html".format(i)
            rep = get_html(url)
            if rep is not None:
                html = etree.HTML(rep)
                tr_list = html.xpath('//table[@class="layui-table"]/tbody/tr')
                for tr in tr_list:
                    ip = tr.xpath('./td[1]/text()')
                    port = tr.xpath('./td[2]/text()')
                    if ip and port:
                        ip_port = ip[0].strip() + ":" + port[0].strip()
                        yield ip_port
                        time.sleep(0.5)

    def crawl_kuaidaili(self):
        for i in range(1, 3):
            url = "https://www.kuaidaili.com/free/inha/{}/".format(i)
            rep = get_html(url)
            if rep is not None:
                html = etree.HTML(rep)
                tr_list = html.xpath('//*[@id="list"]/table/tbody/tr')
                for tr in tr_list:
                    ip = tr.xpath('./td[1]/text()')
                    port = tr.xpath('./td[2]/text()')
                    date = tr.xpath('./td[last()]/text()')
                    if ip and port and date:
                        date = date[0].split(" ")[0]
                        today = str(datetime.datetime.now().date())
                        if date == today:
                            ip_port = ip[0] + ":" + port[0]
                            yield ip_port
                            time.sleep(0.5)

    def crawl_xici(self):
        for i in range(1, 3):
            url = "https://www.xicidaili.com/nn/{}".format(i)
            rep = get_html(url)
            if rep is not None:
                html = etree.HTML(rep)
                tr_list = html.xpath('//*[@id="ip_list"]/tr[@class]')
                for tr in tr_list:
                    ip = tr.xpath('./td[2]/text()')
                    port = tr.xpath('./td[3]/text()')
                    date = tr.xpath('./td[last()]/text()')
                    if ip and port and date:
                        date = datetime.datetime.strptime("20"+date[0].split(" ")[0], "%Y-%m-%d").date()
                        today = datetime.datetime.now().date()
                        if date == today:
                            ip_port = ip[0] + ":" + port[0]
                            yield ip_port
                            time.sleep(0.5)

    def crawl_kaixin(self):
        for i in range(1, 5):
            url = "http://www.kxdaili.com/dailiip/1/{}.html".format(i)
            rep = get_html(url)
            if rep is not None:
                results = re.compile(r'<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>').findall(rep)
                if results:
                    for result in results:
                        ip_port = result[0] + ":" + result[1]
                        yield ip_port
                        time.sleep(0.5)

    def crawl_66ip(self):
        for i in range(1, 6):
            url = "http://www.66ip.cn/areaindex_{}/1.html".format(i)
            rep = get_html(url)
            if rep is not None:
                results = re.compile(r'<tr><td>([\d\.]+)</td><td>(\d+)</td><td>').findall(rep)
                if results:
                    for result in results:
                        ip_port = result[0] + ":" + result[1]
                        yield ip_port
                        time.sleep(0.5)

    def crawl_hai(self):
        url = "http://www.iphai.com/free/ng"
        rep = get_html(url)
        if rep is not None:
            html = etree.HTML(rep)
            tr_list = html.xpath('/html/body/div[2]/div[2]/table/tr')
            for tr in tr_list:
                ip = tr.xpath('./td[1]/text()')
                port = tr.xpath('./td[2]/text()')
                if ip and port:
                    ip_port = ip[0].strip() + ":" + port[0].strip()
                    yield ip_port

    def crawl_xiaoshu(self):
        url = "http://www.xsdaili.com"
        rep = get_html(url)
        if rep is not None:
            html = etree.HTML(rep)
            index = html.xpath('/html/body/div[5]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div[1]/a')[0]
            index_href = index.xpath('./@href')[0]
            url_c = url + index_href
            index_date = index.xpath('./text()')[0].split(" ")[0]
            date = '-'.join(re.findall(r'\d+', index_date))
            today = str(datetime.datetime.now().date())
            if date == today:
                rep = get_html(url_c)
                if rep is not None:
                    results = re.compile(r'<br>\s*(\d+\.\d+\.\d+\.\d+:\d+).*?').findall(rep)
                    if results:
                        for result in results:
                            yield result

    def crawlVpn_66ip(self):
        url = "http://www.66ip.cn/index.html"
        rep = get_html(url)
        if rep is not None:
            results = re.compile(r'<tr><td>([\d\.]+)</td><td>(\d+)</td><td>(.*)</td>').findall(rep)
            if results:
                for result in results:
                    print(result)
                    if result[2][-1] != "市":
                        ip_port = result[0] + ":" + result[1]
                        print(ip_port)




if __name__ == '__main__':
    f = FreeProxyGetter()
    f.crawlVpn_66ip()
    pass
