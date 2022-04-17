#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-04
   开发工具：PyCharm
   功能描述：
-------------------------------------------------
    Change Activity:

-------------------------------------------------
"""
import json
import traceback
import aiohttp
import async_timeout
from book_sentiment_analysis.book_spider.utils import logger
from dataclasses import dataclass
from .exceptions import NothingMatchedError


@dataclass
class Downloader:
    """
    downloader class
    """
    url: str = None
    headers: dict = None
    proxy: str = None
    method: str = None
    body: dict = None
    timeout: int = 5
    encoding: str = 'utf-8'

    def __repr__(self):
        """
        downloader info
        """
        return f'url: {self.url}, proxy: {self.proxy}, encoding: {self.encoding}\n' \
               f' method: {self.method}\n' \
               f' body: {self.body}'

    async def fetch_get(self, client):
        with async_timeout.timeout(self.timeout):
            try:
                if self.method == 'get':
                    async with client.get(self.url, headers=self.headers, proxy=self.proxy,
                                          data=json.dumps(self.body), timeout=self.timeout) as response:
                        assert response.status == 200
                        logger.info(type='Request success!', message='Task url: {}'.format(response.url))
                        response_data = await response.text(encoding=self.encoding, errors='ignore')
                        return response_data
                elif self.method == 'post':
                    async with client.post(self.url, headers=self.headers, proxy=self.proxy,
                                           data=json.dumps(self.body), timeout=self.timeout, allow_redirects=True) as response:
                        assert response.status == 200
                        logger.info(type='Request success!', message='Task url: {}'.format(response.url))
                        response_data = await response.text(encoding=self.encoding, errors='ignore')
                        return response_data
                else:
                    raise NothingMatchedError('Unsupported request method')
            except Exception as e:
                logger.exception(type='Request failed!', message=traceback.format_exc())
                return None

    async def request_by_aiohttp(self):
        """
        Request a url by aiohttp
        :return: html
        """
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as client:
            html = await self.fetch_get(client=client)
            await client.close()
            return html if html else None

    async def request_by_custom(self, method, url, header, body, proxy, timeout):
        """
        Request a url by aiohttp
        :param method: 请求方法
        :param url: 请求头
        :param header: 请求头
        :param timeout: 超时时间
        :param body: 请求参数
        :param proxy: 代理
        :param url: url
        :return: response text
        """
        try:
            async with aiohttp.ClientSession() as session:
                if method == 'get':
                    async with session.get(url, headers=header, proxy=proxy,
                                           data=json.dumps(body), timeout=timeout) as response:
                        assert response.status == 200
                        response_data = await response.text(encoding=self.encoding, errors='ignore')
                elif method == 'post':
                    async with session.get(url, headers=header, proxy=proxy,
                                           ddata=json.dumps(body), timeout=timeout) as response:
                        assert response.status == 200
                        response_data = await response.text(encoding=self.encoding, errors='ignore')
                else:
                    raise NothingMatchedError('Unsupported request method')
                return response_data
        except Exception as e:
            logger.exception(type='Request failed!', message=traceback.format_exc())
            return None
