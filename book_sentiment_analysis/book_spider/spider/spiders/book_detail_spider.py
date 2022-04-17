#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-11
   开发工具：PyCharm
   功能描述：当当网Spider
-------------------------------------------------
    Change Activity:

-------------------------------------------------
"""
import asyncio
import json
import re
from abc import ABC
from datetime import datetime
from lxml import html
from book_sentiment_analysis.book_spider.base_spider import SpiderCore, Downloader, TextField
from book_sentiment_analysis.book_spider.spider.items import BookDetailItem
from book_sentiment_analysis.book_spider.utils import UserAgent
from book_sentiment_analysis import db
from book_sentiment_analysis.models import BookDetail


class DangdangSpider(SpiderCore, ABC):
    # 爬虫名称
    spider_name = 'book_detail_spider'
    # 数据item
    item = BookDetailItem
    # 下载器
    downloader = Downloader()
    # 解析器
    etree = html.etree
    # 请求头初始化
    header = {
        'User-Agent': UserAgent().random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'Connection': 'keep-alive',
        'Host': 'product.dangdang.com',
        'Referer': 'http://search.dangdang.com/',
        'Cookie': '__permanent_id=20220227221202451369604881362582211; dangdang.com=email=MTg3NzYxNzcxNDczNjcxOUBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=&display_id=1162150832510&customerid=FEMUl5DW9xzSyNC3c00xCQ==&viptype=rD/y0bORHUE=&show_name=187****7147; ddscreen=2; USERNUM=lh1WHilKojsUer9rcOkbKA==; login.dangdang.com=.ASPXAUTH=ZxE8Xeh6cmSHnavZ1mHYq6ET7z0qkuzABKp2ldRJE2I9RyYeG5BYHw==; sessionID=pc_3358efe022b897bffa5cff6090e84a4829a5b74c11e83ceed96dcccab41357ac; ddoy=email=1877617714736719@ddmobilphone__user.com&nickname=&validatedflag=0&uname=18776177147&utype=0&.ALFG=off&.ALTM=1650101906913; LOGIN_TIME=1650121404598; __visit_id=20220416230324601336332360197576938; __out_refer=; dest_area=country_id%3D9000%26province_id%3D111%26city_id%3D0%26district_id%3D0%26town_id%3D0; ad_ids=5528526%2C6068312%2C3643543%2C3608930%2C2756405%7C%231%2C3%2C3%2C2%2C1; pos_0_end=1650121427662; pos_9_end=1650121427667; pos_0_start=1650121428581; pos_6_start=1650121434465; pos_6_end=1650121436653; __rpm=s_112100.94003212839%2C94003212840.2.1650121429755%7Cp_1083438557.comment_body..1650121452418; __trace_id=20220416230412530423618482108217948; search_passback=ca5e6b5c7c195f58badc5a62fc01000033d9ca00badc5a62',
    }
    _detail_url = 'http://product.dangdang.com/{}.html'
    # content url
    _content_url = 'http://product.dangdang.com/index.php?r=callback%2Fdetail&' \
                   'productId={productId}&templateType={templateType}&describeMap={describeMap}&' \
                   'shopId={shopId}&categoryPath={categoryPath}'

    async def parse(self):
        """Parse data"""
        # 初始化下载器配置
        self.downloader.method = 'get'
        self.downloader.headers = self.header
        self.downloader.encoding = 'gb2312'
        # 下载详情页
        response_data = await self.downloader.request_by_aiohttp()
        if response_data:
            await self.parse_book_basic_info(response_data)
        # 下载排名信息
        # 调整请求信息
        self.downloader.url = 'http://product.dangdang.com/index.php?r=callback%2Fget-bang-rank&productId={}'.format(
            self.item.sku)
        self.downloader.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        self.downloader.headers['Referer'] = self._detail_url.format(self.item.sku)
        rank_data = await self.downloader.request_by_aiohttp()
        if rank_data:
            await self.parse_book_rank(rank_data)
        else:
            self.item.rank = 'null'
        # 下载内容相关
        # 获取template参数
        template = ''.join(re.findall(r'template\":\"(.*?)\"', response_data))
        # describeMap
        describeMap = ''.join(re.findall(r'describeMap":\"(.*?)\"', response_data))
        # categoryPath
        categoryPath = ''.join(re.findall(r'categoryPath":\"(.*?)\"', response_data))
        self.item.category_path = categoryPath
        self.downloader.url = self._content_url.format(productId=self.item.sku, templateType=template,
                                                       describeMap=describeMap, shopId='0', categoryPath=categoryPath)
        content_data = await self.downloader.request_by_aiohttp()
        if content_data:
            await self.parse_book_content(content_data)

    async def parse_book_basic_info(self, response):
        """Get book info"""
        response_tree = self.etree.HTML(response)
        self.item = self.item(
            img='http:' + TextField(xpath_select='//img[@id="largePic"]/@src', default='').extract(response_tree),
            isbn=TextField(xpath_select='//ul[@class="key clearfix"]/li[5]/text()').extract(response_tree),
            book_name=TextField(
                xpath_select='//div[@id="product_info"]/div[@class="name_info"]/h1/@title').extract(response_tree),
            abstract_title=TextField(
                xpath_select='//span[@class="head_title_name"]/text()', default='').extract(response_tree),
            author=TextField(xpath_select='//span[@id="author"]/a/text()', default='null').extract(response_tree),
            publisher=TextField(xpath_select='//span[@dd_name="出版社"]/a', default='null').extract(response_tree),
            publication_date=TextField(xpath_select='//span[@class="t1"][3]', default='null').extract(response_tree).strip(),
            price=TextField(xpath_select='//p[@id="dd-price"]').extract(response_tree).strip(),
            classification=TextField(
                xpath_select='//li[@id="detail-category-path"]/span[@class="lie"]',
                default='null').extract(response_tree))
        # 清洗，预处理
        self.item.isbn = self.item.isbn.replace('国际标准书号ISBN：', '')
        self.item.abstract_title = self.item.abstract_title.replace('\r', '').replace('\n', '').replace('\t',
                                                                                                        '').strip()
        self.item.publication_date = self.item.publication_date.replace('出版时间:', '')
        self.item.price = self.item.price.replace('¥', '')

    async def parse_book_rank(self, response):
        """Get rank info"""
        rank_data = json.loads(response)
        path_name = rank_data.get('data').get('pathName', '')
        rank = rank_data.get('data').get('rank', '')
        self.item.rank = '在当当网' + path_name + '排名第' + rank

    async def parse_book_content(self, response):
        """Get book content"""
        content_data = json.loads(response).get('data').get('html')
        self.item.content = ''.join(re.findall(r'<span id=\"content-all\"><\/span><p>(.*?)<\/p>', content_data))
        self.item.catalogue = ''.join(re.findall(r'<span id=\"catalog-show\">(.*?)<\/span>', content_data))
        self.item.preface = ''.join(re.findall(r'<span id=\"preface-show\">(.*?)<\/span>', content_data))

    async def save(self):
        """Save data"""
        book = BookDetail(sku=self.item.sku, category_path=self.item.category_path, img=self.item.img,
                          isbn=self.item.isbn, book_name=self.item.book_name, abstract_title=self.item.abstract_title,
                          author=self.item.author, publisher=self.item.publisher,
                          publication_date=self.item.publication_date, price=self.item.price, rank=self.item.rank,
                          classification=self.item.classification, content=self.item.content,
                          catalogue=self.item.catalogue, preface=self.item.preface)
        db.session.add(book)
        db.session.commit()

    async def start(self, sku):
        """Start a spider"""
        start_time = datetime.now()
        # 初始化爬取的url
        self.item.sku = sku
        self.downloader.url = self._detail_url.format(sku)
        self.logger.info(type='Spider started', message=self.spider_name + " Crawling...")
        await self.parse()
        await self.save()
        self.logger.info(type='Spider finished',
                         message='Time usage：{seconds}'.format(seconds=(datetime.now() - start_time)))


async def run(sku):
    """
    Start spider
    """
    spider = DangdangSpider()
    await spider.start(sku)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run('29222668'))
    loop.close()
