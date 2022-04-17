#!/usr/bin/env python
"""
 book spider
 Created by janeho at 14/03/2022.
"""
from book_sentiment_analysis.book_spider.spider.spiders.book_search_spider import run as search_spider
from book_sentiment_analysis.book_spider.spider.spiders.book_detail_spider import run as detail_spider
from book_sentiment_analysis.book_spider.spider.spiders.book_comments_spider import run as comment_spider

