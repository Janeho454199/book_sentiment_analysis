"""
 data process model
 Created by janeho at 11/04/2022.
"""
import numpy as np
from sqlalchemy import and_
from .base_response import BaseResponse
from book_sentiment_analysis.models import WordCount, Sentiment, Keyword, Comments


class DataProcess(BaseResponse):

    def __init__(self, sku):
        super().__init__()
        self.sku = sku
        self.data = {}

    def data_process(self):
        self.data['word_count'] = self.get_word_cloud()
        self.data['positive_rate'] = self.get_positive_rate_pie()
        self.data['sentiment_distribution'] = self.get_sentiment_scatter()
        self.data['keyword'] = self.get_keyword()
        self.data['summary'] = self.get_summary()
        self.data['radar_sentiment'] = self.get_sentiment_radar()
        self.data['praise_comment'] = self.get_praise()
        self.data['medium_comment'] = self.get_medium()
        self.data['negative_comment'] = self.get_negative()

        return self.data

    def get_word_cloud(self):
        """
        get data for word-cloud
        :return: list[dict, dict, dict]
        """
        result = []
        word_count = WordCount.query.filter_by(sku=self.sku).all()
        for word in word_count:
            k, v = word.word, word.index
            result.append({"name": k,
                           "value": v})
        return result

    def get_positive_rate_pie(self):
        """
        get Feedback Rate for pie
        :return: dict
        """
        result = {}
        pos = 0
        neg = 0
        data = Sentiment.query.filter_by(sku=self.sku).all()
        for sentiment in data:
            if sentiment.sentiment > 0.5:
                pos += 1
            else:
                neg += 1

        result['pos'] = round((pos/(pos+neg)) * 100)
        result['neg'] = round((neg/(pos+neg)) * 100)
        return result

    def get_sentiment_scatter(self):
        """
        get data for scatter
        :return: list[list]
        """
        result = []
        sentiment_dict_list = {round(k, 2): 0 for k in np.arange(0.00, 1.01, 0.01)}
        sentiment_data = Sentiment.query.filter_by(sku=self.sku).all()
        for sentiment in sentiment_data:
            sentiment_dict_list[round(sentiment.sentiment, 2)] += 1
        # 转list
        for i in sentiment_dict_list.keys():
            if sentiment_dict_list[i] != 0:
                result.append([i, sentiment_dict_list[i]])
        return result

    def get_keyword(self):
        """
        get comment keyword
        :return: str
        """
        keyword_data = Keyword.query.filter_by(sku=self.sku).first()
        result = keyword_data.keyword
        return result

    def get_summary(self):
        """
        get comment summary
        :return: str
        """
        summary_data = Keyword.query.filter_by(sku=self.sku).first()
        result = summary_data.summary
        return result

    def get_sentiment_radar(self):
        """
        get radar data
        :return: list
        """
        sentiment = Sentiment.query.filter_by(sku=self.sku).all()
        sentiment_list = [round(index.sentiment, 2) for index in sentiment]
        # 最高倾向
        max_sentiment = max(sentiment_list)
        # 中位数
        medium_sentiment = np.median(sentiment_list)
        # 平均数
        average_sentiment = np.mean(sentiment_list)
        # 众数
        mode_sentiment = max(set(sentiment_list),key=sentiment_list.count)
        # 最低倾向
        min_sentiment = min(sentiment_list)

        return [max_sentiment, medium_sentiment, average_sentiment, mode_sentiment, min_sentiment]

    def get_praise(self):
        """
        get the comment with the highest score
        :return: str
        """
        most_positive_sentiment = 0
        most_positive_id = 0
        sentiment = Sentiment.query.filter_by(sku=self.sku).all()
        for index in sentiment:
            if index.sentiment > most_positive_sentiment:
                most_positive_sentiment = index.sentiment
                most_positive_id = index.comment_id
        comment = Comments.query.filter_by(id=most_positive_id).first()

        return comment.comment

    def get_negative(self):
        """
        get the comment with the lowest score
        :return: str
        """
        sentiment = Sentiment.query.filter_by(sku=self.sku).all()
        sentiment_list = [index.sentiment for index in sentiment]
        min_sentiment = min(sentiment_list)
        comment_id = Sentiment.query.filter_by(sentiment=min_sentiment).first().comment_id
        comment = Comments.query.filter(and_(Comments.sku == self.sku, Comments.id == comment_id)).first()

        return comment.comment

    def get_medium(self):
        """
        get medium comments
        :return: str
        """
        sentiment = Sentiment.query.filter_by(sku=self.sku).all()
        for index in sentiment:
            if 0.45 <= index.sentiment <= 0.55:
                comment_id = index.comment_id
                return Comments.query.filter(and_(Comments.sku == self.sku, Comments.id == comment_id)).first().comment

        return ''

if __name__ == '__main__':
    test = DataProcess('28486010')
    data = test.get_sentiment_radar()
    print(data)