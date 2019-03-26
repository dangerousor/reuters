#!/usr/bin/python
# -*- coding:utf-8 -*-
from lxml import etree
import requests
import os


class Spider:
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}

    def get_html(self, url):
        return requests.get(url, headers=self.header, timeout=30)

    @staticmethod
    def parse_html(content):
        html = etree.HTML(content)
        return html.xpath('//*[@id="blogStyleNews"]/section/div/article')

    @staticmethod
    def get_time(article):
        return article.xpath('./div[2]/time/span/text()')[0]

    @staticmethod
    def make_path(p):
        if os.path.exists(p):  # 判断文件夹是否存在
            return
        os.mkdir(p)

    def save(self, t, article):
        url = 'https://cn.reuters.com' + article.xpath('./div[2]/a/@href')[0]
        title = article.xpath('./div[2]/a/h3/text()')[0].encode().decode().replace('\n', '').replace('\t', '')
        # print(title.replace('\n', '').replace('\t', ''))
        html = self.get_html(url)
        contents = etree.HTML(html.content.decode()).xpath('//*[@class="StandardArticleBody_body"]/p')
        content = []
        for each in contents:
            content.append(each.xpath('string(.)').encode())
        if content:
            temp = content[0].split('-'.encode(), 1)
            if temp[0].strip().startswith('路透'.encode()):
                content[0] = temp[1].strip()
        self.make_path(os.path.join('data', t))
        with open(os.path.join('data', t, title + '.txt'), 'wb+') as f:
            f.write('\n'.encode().join(content))
            f.write('\n'.encode())

    def run(self):
        i = 22
        start = True
        end = True
        while start or end:
            url = 'https://cn.reuters.com/news/archive/chinaNews?view=page&page=%s&pageSize=10' % i
            html = self.get_html(url)
            if html.status_code != 200:
                print(html.content)
                print(html.status_code)
                exit(-1)
            res = self.parse_html(html.content.decode())
            for each in res:
                t = self.get_time(each).replace(' ', '')
                if start:
                    if t == '2019年2月28日':
                        start = False
                    else:
                        continue
                else:
                    if t == '2014年12月31日':
                        end = False
                        break
                self.save(t, each)
                print(t)
            i = i + 1


if __name__ == '__main__':
    spider = Spider()
    spider.make_path('data')
    spider.run()
