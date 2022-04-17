"""
 Data model
 Created by janeho at 14/03/2022.
"""
from book_sentiment_analysis import db


class Book(db.Model):
    # sku
    sku = db.Column(db.String(10), primary_key=True)
    # img
    img = db.Column(db.String(60))
    # 书名
    book_name = db.Column(db.String(120))
    # 作者
    author = db.Column(db.String(60))
    # 出版社
    publisher = db.Column(db.String(20))
    # 出版时间
    publication_date = db.Column(db.String(20))
    # 价格
    price = db.Column(db.String(10))
    # 评分
    score = db.Column(db.String(10))
    # 评论数
    reviews_count = db.Column(db.String(10))
    # url
    url = db.Column(db.String(120))


class BookDetail(db.Model):
    # sku
    sku = db.Column(db.String(10), primary_key=True)
    # categoryPath
    category_path = db.Column(db.String(20))
    # img
    img = db.Column(db.String(60))
    # ISBN
    isbn = db.Column(db.String(10))
    # 书名
    book_name = db.Column(db.String(120))
    # abstract_title
    abstract_title = db.Column(db.String(180))
    # 作者
    author = db.Column(db.String(20))
    # 出版社
    publisher = db.Column(db.String(20))
    # 出版时间
    publication_date = db.Column(db.String(20))
    # 价格
    price = db.Column(db.String(10))
    # rank
    rank = db.Column(db.String(20))
    # 所属分类
    classification = db.Column(db.String(60))
    # content
    content = db.Column(db.String(255))
    # 目录
    catalogue = db.Column(db.String(255))
    # 前言
    preface = db.Column(db.String(255))


class Comments(db.Model):
    # id
    id = db.Column(db.Integer, primary_key=True)
    # sku
    sku = db.Column(db.String(10))
    # 评分
    score = db.Column(db.String(10))
    # 评论
    comment = db.Column(db.String(255))
    # 评论时间
    date = db.Column(db.String(20))
    # 用户名
    user_name = db.Column(db.String(30))
    # 入库时间
    etl_date = db.Column(db.Date)


class WordCount(db.Model):
    # id
    id = db.Column(db.Integer, primary_key=True)
    # sku
    sku = db.Column(db.String(10))
    # 词
    word = db.Column(db.String(30))
    # 频
    index = db.Column(db.Integer)


class Sentiment(db.Model):
    # id
    id = db.Column(db.Integer, primary_key=True)
    # comment_id
    comment_id = db.Column(db.Integer)
    # sku
    sku = db.Column(db.String(10))
    # sentiment
    sentiment = db.Column(db.Float)


class Keyword(db.Model):
    # sku
    sku = db.Column(db.String(10), primary_key=True)
    # keyword
    keyword = db.Column(db.String(60))
    # summary
    summary = db.Column(db.String(120))
