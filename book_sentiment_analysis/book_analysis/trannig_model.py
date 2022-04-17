"""
 train method
 Created by janeho at 07/04/2022.
"""
from snownlp import sentiment


def start_train():
    """
    读取语料库重新训练模型
    """
    sentiment.train('./corpus/neg.txt', './corpus/pos.txt')
    sentiment.save('sentiment.marshal')


# 词频表（sku， word， index， type（1好评，0差评））

# 评论分析表（sku， id， sentiment）
# 评分表（sku， pos， neg， rate）

# 关键字、句表（sku， keyword， summary）

# 爬虫爬取数据————》分析模块————》评论分析表（记录每一个商品下的每一条评论的情感倾向）
# ————》计算出评分表（饼图，散点图），词频表（词云图），关键字句表（关键词），

"""
    词云图需要的{
        name: 词,
        value: 频
    }
"""

