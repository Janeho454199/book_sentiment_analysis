#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-10
   开发工具：PyCharm
   功能描述：当当网Spider
-------------------------------------------------
    Change Activity:

-------------------------------------------------
"""
import asyncio
from abc import ABC
from datetime import datetime
from lxml import html
from book_sentiment_analysis.book_spider.base_spider import SpiderCore, Downloader, TextField
from book_sentiment_analysis.book_spider.spider.items import BookItem
from book_sentiment_analysis.book_spider.utils import UserAgent
from book_sentiment_analysis.models import Book
from book_sentiment_analysis import db


class DangdangSpider(SpiderCore, ABC):
    # 爬虫名称
    spider_name = 'book_comment_spider'
    # 数据item
    item = BookItem
    # 下载器
    downloader = Downloader()
    # 解析器
    etree = html.etree
    # 请求头初始化
    header = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'search.dangdang.com',
        'Referer': 'http://www.dangdang.com/',
        'Cookie': '__permanent_id=20220111170358640108346369623943594; cart_id=4000000007615869806; secret_key=a055d042932726b36e7bf42de60ef989; dangdang.com=email=MTg3NzYxNzcxNDczNjcxOUBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=&display_id=1162150832510&customerid=FEMUl5DW9xzSyNC3c00xCQ==&viptype=rD/y0bORHUE=&show_name=187****7147; ddscreen=2; __visit_id=20220415160150495189741980609203285; __out_refer=; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0; pos_9_end=1650009848375; pos_0_start=1650009848387; pos_0_end=1650009848395; ad_ids=5528526%2C6068312%2C3643543%7C%232%2C3%2C1; sessionID=pc_6afc24996bdfc64caf945c5e816a2804a6903fa2b3c714063aab596143d35ecd; USERNUM=lh1WHilKojsUer9rcOkbKA==; login.dangdang.com=.ASPXAUTH=ZxE8Xeh6cmSHnavZ1mHYq6ET7z0qkuzABKp2ldRJE2I9RyYeG5BYHw==; ddoy=email=1877617714736719@ddmobilphone__user.com&nickname=&validatedflag=0&uname=18776177147&utype=0&.ALFG=off&.ALTM=1650009921410; LOGIN_TIME=1650009937217; __rpm=%7Cs_112100.94003212839%2C94003212840.2.1650009942114; __trace_id=20220415160543360299474869937512381',
    }
    # 搜索url
    _search_url = 'http://search.dangdang.com/?key={}&act=input&page_index={}'
    # 代理
    proxy = {}
    # 爬取的结果
    results = []

    async def parse(self):
        """Parse data"""
        # 初始化下载器配置
        self.downloader.method = 'get'
        self.downloader.headers = self.header
        self.downloader.encoding = 'gb2312'
        # 下载搜索页面
        response_data = await self.downloader.request_by_aiohttp()
        if response_data:
            # 解析书本列表
            self.results = await self.parse_book_list(response_data)

    async def parse_book_list(self, response):
        """Get book list"""
        response_tree = self.etree.HTML(response)
        # book_list
        item_list = response_tree.xpath('//ul[@class="bigimg"]/li')
        book_result = []
        for item in item_list:
            book_info = self.item(
                sku=TextField(xpath_select='./@id').extract(item).replace('p', ''),
                img='https:' + TextField(xpath_select='./a/img/@data-original', default='null').extract(item),
                book_name=TextField(xpath_select='./a/@title').extract(item),
                author=TextField(xpath_select='./p/span/a[@name="itemlist-author"]/@title', default='null').extract(item),
                publisher=TextField(xpath_select='./p/span/a[@name="P_cbs"]/@title', default='null').extract(item),
                publication_date=TextField(
                    xpath_select='./p[@class="search_book_author"]/span[2]/text()', default='null').extract(item),
                price=TextField(
                    xpath_select='./p[@class="price"]/span[@class="search_now_price"]/text()', default='0').extract(item),
                score=TextField(
                    xpath_select='./p/span[@class="search_star_black"]/span/@style', default='width: 0%').extract(item),
                reviews_count=TextField(xpath_select='./p/a[@class="search_comment_num"]/text()', default='0').extract(item),
                url='https:' + TextField(xpath_select='./p[@class="name"]/a/@href').extract(item)
            )
            # 图片信息特殊处理
            if book_info.img == 'https:null':
                book_info.img = 'https:' + TextField(xpath_select='./a/img/@src', default='null').extract(item)
            # 清洗,预处理
            book_info.publication_date = book_info.publication_date.replace('/', '')
            book_info.price = book_info.price.replace('¥', '')
            book_info.score = book_info.score.replace('width:', '').replace('%;', '')
            book_info.reviews_count = book_info.reviews_count.replace('条评论', '')
            book_result.append(book_info)

        return book_result

    async def save(self):
        """Save data"""
        # 执行搜索爬虫的时候，每一次都清空数据库表
        Book.query.delete()
        for book in self.results:
            book = Book(sku=book.sku, img=book.img, book_name=book.book_name, author=book.author,
                        publisher=book.publisher, publication_date=book.publication_date, price=book.price,
                        score=book.score, reviews_count=book.reviews_count, url=book.url)
            db.session.add(book)
        db.session.commit()

    async def start(self, keyword, page):
        """Start a spider"""
        start_time = datetime.now()
        # 初始化爬取的url
        self.downloader.url = self._search_url.format(keyword, page)
        # 如遇翻页，调整Referer
        if page > 1:
            self.header['Referer'] = self._search_url.format(keyword, page)
        self.logger.info(type='Spider started', message=self.spider_name + " Crawling...")
        await self.parse()
        await self.save()
        self.logger.info(type='Spider finished',
                         message='Time usage：{seconds}'.format(seconds=(datetime.now() - start_time)))


async def run(keyword, page):
    """
    Start spider
    """
    spider = DangdangSpider()
    await spider.start(keyword, page)
    return spider


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run('老人与海', 1))
    loop.close()
