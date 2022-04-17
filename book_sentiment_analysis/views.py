"""
 view
 Created by janeho at 14/03/2022.
"""
import asyncio
import traceback
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, jsonify
from book_sentiment_analysis import app
from book_sentiment_analysis.book_spider import search_spider, detail_spider, comment_spider
from book_sentiment_analysis.book_analysis import AnalysisModel
from book_sentiment_analysis.book_restful import DataProcess
from book_sentiment_analysis.models import Book, BookDetail, Comments
from book_sentiment_analysis import db


@app.route('/')
def index():
    """
    Index
    """
    books = Book.query.all()
    return render_template('index.html', books=books)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    Search book
    """
    if request.form['keyword']:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(search_spider(request.form['keyword'], 1))
        loop.close()
        books = Book.query.all()
        return render_template('index.html', books=books)
    else:
        flash('Invalid input.')


@app.route('/detail')
def detail():
    """
    Book detail
    """
    sku = request.args.get('sku')
    # 书本收录标志（已收录则直接返回，未收录则爬取信息）
    exist = BookDetail.query.filter_by(sku=sku).first()
    if exist:
        book = BookDetail.query.get_or_404(sku)
        return render_template('detail.html', book=book)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(detail_spider(sku))
        loop.close()
        book = BookDetail.query.get_or_404(sku)
        return render_template('detail.html', book=book)


@app.route('/detail/analysis/<string:sku>', methods=['POST'])
def analysis(sku):
    """
    Analysis book
    """
    # 获取书本信息
    book = BookDetail.query.get_or_404(sku)
    # 判断书本是否支持分析(评论数小于400则没有分析的必要)
    book_reviews_count = Book.query.filter_by(sku=sku).first().reviews_count
    # 数据处理模块
    process = DataProcess(sku)
    if int(book_reviews_count) < 400:
        return process.fail(data='Not enough reviews for analysis.')
    # 实例化分析模块
    analysis_model = AnalysisModel()
    # 书本收录标志（已收录则直接返回，未收录则爬取信息）
    exist = Comments.query.filter_by(sku=sku).first()

    # 生成循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # 距离上次爬取日期超过三十天则清除后重新爬取
    try:
        if exist:
            etl_date = exist.etl_date.day
            cur_date = datetime.today().date().day
            if (cur_date - etl_date) <= 30:
                # 数据处理
                result = process.data_process()
                return process.success(data=result)
            else:
                Comments.query.filter_by(sku=sku).delete()
                db.session.commit()
                loop.run_until_complete(comment_spider(book.sku, book.category_path))
        else:
            loop.run_until_complete(comment_spider(book.sku, book.category_path))
        loop.close()
        # 数据分析
        analysis_model.analysis_sentiment(sku)
        analysis_model.word_count(sku)
        analysis_model.analysis_abstract(sku)
        # 数据处理
        result = process.data_process()
    except Exception as e:
        print(traceback.format_exc(e))
        return process.fail(data='An error occurred. Please try again!')
    return process.success(data=result)
