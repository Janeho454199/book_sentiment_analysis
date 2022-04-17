#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-09
   开发工具：PyCharm
   功能描述：当当网ITEM
-------------------------------------------------
    Change Activity:

-------------------------------------------------
"""
from book_sentiment_analysis.book_spider.base_spider.item import Item, StringField, IntegerField


class BookItem(Item):
    # sku
    sku = StringField
    # img
    img = StringField
    # 书名
    book_name = StringField
    # 作者
    author = StringField
    # 出版社
    publisher = StringField
    # 出版时间
    publication_date = StringField
    # 价格
    price = IntegerField
    # 当当评分
    score = IntegerField
    # 评论数
    reviews_count = StringField
    # 书本链接
    url = StringField


class BookDetailItem(Item):
    # img
    img = StringField
    # categoryPath
    category_path = StringField
    # sku
    sku = StringField
    # ISBN
    isbn = StringField
    # 书名
    book_name = StringField
    # abstract_title
    abstract_title = StringField
    # 作者
    author = StringField
    # 出版社
    publisher = StringField
    # 出版时间
    publication_date = StringField
    # 价格
    price = IntegerField
    # rank
    rank = StringField
    # 所属分类
    classification = StringField
    # content
    content = StringField
    # 目录
    catalogue = StringField
    # 前言
    preface = StringField


class CommentItem(Item):
    # sku
    sku = StringField
    # 评分
    score = IntegerField
    # 评论
    comment = StringField
    # 评论时间
    date = StringField
    # 用户名
    user_name = StringField
