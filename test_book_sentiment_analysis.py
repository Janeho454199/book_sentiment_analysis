import numpy as np
import requests
from snownlp import SnowNLP

from book_sentiment_analysis.models import Comments, Sentiment
from sqlalchemy import and_

data = Comments.query.filter_by(sku='29206214').all()

# for i in data:
#     sentiment_data = Sentiment.query.filter_by(comment_id=i.id).first()
#     sentiment = 1 if sentiment_data.sentiment > 0.5 else 0
#     if sentiment == 0:
#         print(i.comment)

# s = SnowNLP('改造耐烦纵横圣贤丰登放手多情懂行辅助得名修身绵长金口五彩雅言风姿盖世奇崛')
#
# print(s.keywords())

for i in range(1000):
    proxy_url = 'http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=0&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=110000,120000,130000,150000,210000,220000,230000,310000,320000,330000,340000,350000,360000,370000,410000,420000,430000,440000,450000,460000,500000,510000,520000,610000,630000&username=chukou01&spec=1'

    response = requests.get(proxy_url)
    print(response.text)