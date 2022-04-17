"""
 analysis model
 Created by janeho at 08/04/2022.
"""
import os
import jieba
from book_sentiment_analysis import db
from snownlp import SnowNLP
from book_sentiment_analysis.models import Comments, WordCount, Sentiment, Keyword


class AnalysisModel:
    """
    analysis
    """

    def __init__(self):
        current_path = os.path.dirname(__file__)
        # 加载停用词表
        self.stop_word = open(current_path + '/corpus/stop_word.txt')
        self.stop_word_list = set(line.strip() for line in self.stop_word)
        # 添加词典提升准确度
        self.word_dict = open(current_path + '/corpus/dict.txt')
        for word in self.word_dict:
            jieba.add_word(word)

    def sub_word(self, word_dict, word_list):
        """
        sub word and gather word count
        :param word_dict: word dict
        :param word_list: word list
        :return:
        """
        if not word_list:
            return

        for word in word_list:
            # 跳过停用词
            if word in self.stop_word_list:
                continue
            else:
                if word_dict.get(word, 0):
                    word_dict[word] += 1
                else:
                    word_dict[word] = 1

    @staticmethod
    def analysis_sentiment(sku):
        """
        start analysis sentiment
        :param sku: book sku
        """
        # 筛选
        comments = Comments.query.filter_by(sku=sku).all()
        for comment in comments:
            s = SnowNLP(comment.comment)
            # 获取情感倾向
            sentiment_score = s.sentiments
            sentiment = Sentiment(comment_id=comment.id, sku=sku, sentiment=sentiment_score)
            db.session.add(sentiment)
        db.session.commit()

    def word_count(self, sku):
        """
        start word count
        :param sku: book sku
        """
        word_data = {}
        # 筛选
        comments = Comments.query.filter_by(sku=sku).all()
        for comment in comments:
            # 分词
            comment_word = jieba.lcut(comment.comment, cut_all=False)
            self.sub_word(word_data, comment_word)
        for word in word_data.keys():
            word_count = WordCount(sku=sku, word=word, index=word_data[word])
            db.session.add(word_count)

        db.session.commit()

    def analysis_abstract(self, sku):
        """
        start analysis abstract and keyword
        :param sku: book sku
        """
        # 筛选
        comments = Comments.query.filter_by(sku=sku).all()
        text = ''

        # 拼接所有评论
        for comment in comments:
            text += '。' + comment.comment

        # 分词
        keyword_text = ''.join([word if word not in self.stop_word_list else '' for word in jieba.lcut(text, cut_all=False)])

        keyword_data = SnowNLP(keyword_text)
        summary_data = SnowNLP(text)
        db.session.add(Keyword(sku=sku, keyword=','.join(keyword_data.keywords(4)), summary=','.join(summary_data.summary(3))))
        db.session.commit()


if __name__ == '__main__':
    analysis_model = AnalysisModel()
    analysis_model.analysis_abstract(sku='28486010')
