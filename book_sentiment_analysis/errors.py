# -*- coding: utf-8 -*-
"""
 error
 Created by janeho at 14/03/2022.
"""
from flask import render_template
from book_sentiment_analysis import app


@app.errorhandler(400)
def bad_request(e):
    return render_template('/400.html'), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('/500.html'), 500