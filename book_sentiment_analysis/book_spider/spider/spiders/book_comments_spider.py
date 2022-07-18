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
from abc import ABC
from aiohttp.client_exceptions import ClientOSError
from lxml import html
from datetime import datetime
from book_sentiment_analysis.book_spider.base_spider import SpiderCore, Downloader, TextField
from book_sentiment_analysis.book_spider.spider.items import CommentItem
from book_sentiment_analysis.book_spider.utils import UserAgent
from book_sentiment_analysis.models import Comments
from book_sentiment_analysis import db


class DangdangSpider(SpiderCore, ABC):
    # 爬虫名称
    spider_name = 'book_comments_spider'
    # 数据item
    item = CommentItem
    # 下载器
    downloader = Downloader()
    # 代理
    proxy_url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=2&pro=0&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=440000'
    # 解析器
    etree = html.etree
    # 初始化请求头
    header = {
        'User-Agent': UserAgent().random,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'Connection': 'keep-alive',
        'Host': 'product.dangdang.com',
        'Referer': 'https://product.dangdang.com/{}.html',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': '__permanent_id=20220227221202451369604881362582211; dangdang.com=email=MTg3NzYxNzcxNDczNjcxOUBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=&display_id=1162150832510&customerid=FEMUl5DW9xzSyNC3c00xCQ==&viptype=rD/y0bORHUE=&show_name=187****7147; dest_area=country_id%3D9000%26province_id%3D111%26city_id%20%3D0%26district_id%3D0%26town_id%3D0; __visit_id=20220430080252497561340167363510137; __out_refer=; __rpm=%7Clogin_page...1651276974089; sessionID=pc_52ecd9f98183f5a8edf1d106035e0cca1d53d5ea74e142653adf6d30d21da955; USERNUM=lh1WHilKojsUer9rcOkbKA==; login.dangdang.com=.ASPXAUTH=ZxE8Xeh6cmSHnavZ1mHYq6ET7z0qkuzABKp2ldRJE2I9RyYeG5BYHw==; ddoy=email=1877617714736719@ddmobilphone__user.com&nickname=&validatedflag=0&uname=18776177147&utype=0&.ALFG=off&.ALTM=1651276980193; secret_key=83b8669ee73e43636462054c3df7181c; ddscreen=2; LOGIN_TIME=1651276984123; __trace_id=20220430080308218428488561120790799',
    }
    # url
    _comment_url = 'http://product.dangdang.com/index.php?r=comment%2Flist&productId={productId}&' \
                   'categoryPath={categoryPath}&mainProductId={mainProductId}&mediumId=0&' \
                   'pageIndex={pageIndex}&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish'
    results = []

    async def parse(self, sku, category_path):
        """Parse data"""
        # 初始化下载器配置
        self.downloader.method = 'get'
        self.downloader.encoding = 'utf-8'
        self.downloader.headers = self.header
        # 默认爬取500页
        for page_index in range(1, 100):
            await asyncio.sleep(0.5)
            # 获取代理
            try:
                proxy_data = json.loads(await self.downloader.request_by_custom(method='get', url=self.proxy_url, header='', body='', proxy='', timeout=20))
                print(proxy_data)
                self.downloader.proxy = 'http://' + proxy_data['data'][0]['ip'] + ':' + str(
                    proxy_data['data'][0]['port'])
            except:
                pass
            self.downloader.url = self._comment_url.format(productId=sku, categoryPath=category_path,
                                                           mainProductId=sku, pageIndex=page_index)
            try:
                comment_data = await self.downloader.request_by_aiohttp()
                if comment_data:
                    comment_data = json.loads(comment_data)
                    # 循环结束
                    if page_index > int(comment_data.get('data').get('list').get('summary').get('pageCount')):
                        break
                    comments = await self.parse_comment(comment_data)
                    self.results.extend(comments)
            except (ClientOSError, Exception):
                continue

    async def parse_comment(self, response):
        """Get rank info"""
        comments = []
        response_tree = self.etree.HTML(response.get('data').get('list').get('html'))
        comments_list = response_tree.xpath('//div[@class="item_wrap"]/div[@class="comment_items clearfix"]')
        for comment in comments_list:
            comment_info = self.item(
                sku=response.get('data').get('list').get('summary').get('main_product_id'),
                score=TextField(
                    xpath_select='./div[@class="items_right"]/div[@class="pinglun"]/em/text()').extract(comment),
                comment=TextField(
                    xpath_select='./div[@class="items_right"]/div[@class="describe_detail"]/span/a/text()').extract(comment),
                date=TextField(
                    xpath_select='./div[@class="items_right"]/div[@class="starline clearfix"]/span/text()').extract(comment),
                user_name=TextField(
                    xpath_select='./div[@class="items_left_pic"]/span[@class="name"]/text()').extract(comment)
            )
            print(comment_info.sku, comment_info.score,
                  comment_info.comment, comment_info.date, comment_info.user_name)
            comments.append(comment_info)

        return comments

    async def save(self):
        """Save data"""
        for comment in self.results:
            comment = Comments(sku=comment.sku, score=comment.score, comment=comment.comment, date=comment.date,
                               user_name=comment.user_name, etl_date=datetime.today().date())
            db.session.add(comment)
        db.session.commit()

    async def start(self, sku, category_path):
        """Start a spider"""
        start_time = datetime.now()
        self.logger.info(type='Spider started', message=self.spider_name + " Crawling...")
        self.header['Referer'] = self.header['Referer'].format(sku)
        await self.parse(sku, category_path)
        await self.save()
        self.logger.info(type='Spider finished',
                         message='Time usage：{seconds}'.format(seconds=(datetime.now() - start_time)))


async def run(sku, category_path):
    """
    Start spider
    """
    spider = DangdangSpider()
    await spider.start(sku, category_path)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run('28496042', '01.43.77.07.00.00'))
    loop.close()
