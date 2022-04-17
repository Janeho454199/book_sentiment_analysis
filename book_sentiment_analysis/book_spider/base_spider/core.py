#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-04
   开发工具：PyCharm
   功能描述：爬虫基础类
-------------------------------------------------
    Change Activity:

-------------------------------------------------
"""
import abc
from book_sentiment_analysis.book_spider.utils import logger


class SpiderCore(metaclass=abc.ABCMeta):
    """
    Spider
    """
    spider_name = None
    item = None
    logger = logger

    def __init__(self):
        if not getattr(self, 'spider_name', None):
            raise ValueError('Spider must have a spider_name')
        if not getattr(self, 'item', None):
            raise ValueError('Spider must have a item')
        setattr(self, 'spider_name', self.spider_name)
        setattr(self, 'item', self.item)
        setattr(self, 'logger', self.logger)

    @abc.abstractmethod
    async def parse(self, **kw):
        """It is a necessary method"""
        raise NotImplementedError

    @abc.abstractmethod
    async def save(self, **kw):
        """It is a necessary method"""
        raise NotImplementedError

    @abc.abstractmethod
    async def start(self, **kw):
        """Start a spider"""
        raise NotImplementedError
