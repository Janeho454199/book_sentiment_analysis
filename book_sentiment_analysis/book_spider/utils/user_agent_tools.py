#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-10
   开发工具：PyCharm
   功能描述：生成随机请求头
-------------------------------------------------
    Change Activity:
        2022/03/24: 变为从fake_useragent获取随机请求头
-------------------------------------------------
"""
import asyncio
from book_sentiment_analysis.book_spider.base_spider.exceptions import FakeUserAgentError
from .public_tools import singleton
from fake_useragent import UserAgent as FakeUserAgent


@singleton
class UserAgent(object):
    """
    获取随机请求头
    """

    def __init__(self):
        """
        初始化
        """
        try:
            self.ua = FakeUserAgent()
            self.random = asyncio.run(self._get_data())
        except FakeUserAgentError:
            raise FakeUserAgentError('Exception getting request header')
        # self.current_path = os.path.dirname(__file__)
        # self.json_file = self.current_path + '/fake_user_agent.json'
        # self.ua_data = asyncio.run(self._get_data())
        # self.ua_data = self.ua_data.get("browsers")
        # self.browser = ['chrome', 'opera', 'firefox', 'safari', 'internetexplorer']
        # self.chrome = lambda: random.choice(self.ua_data.get("chrome"))
        # self.opera = lambda: random.choice(self.ua_data.get("opera"))
        # self.firefox = lambda: random.choice(self.ua_data.get("firefox"))
        # self.safari = lambda: random.choice(self.ua_data.get("safari"))
        # self.ie = lambda: random.choice(self.ua_data.get("internetexplorer"))
        # self.random = lambda: random.choice(self.ua_data.get(random.choice(self.browser)))

    async def _get_data(self):
        """
        Get random UserAgent
        :return: read data
        """
        # try:
        #     async with aiofiles.open(self.json_file, mode='r') as f:
        #         data = await f.read()
        # except:
        #     data = dict()
        return self.ua.random
