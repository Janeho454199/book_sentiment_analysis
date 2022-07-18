# book_sentiment_analysis

图书情感分析，通过爬取当当网的图书信息，评论等数据，进行情感分析表并展示

## Installation

本地环境是在Linux上使用的[conda](https://github.com/conda/conda)作为包管理器，不依赖conda可以自行将yaml中的依赖转换

```
conda env create -f environment.yaml
```

环境在environment.yaml中，用conda导入即可（有多余的环境，未作环境隔离）

:warning:请自行替换代理和cookie，具体替换方法可以查看[下载器](https://github.com/Janeho454199/book_sentiment_analysis/blob/main/book_sentiment_analysis/book_spider/base_spider/downloader.py)和[爬虫主程序](https://github.com/Janeho454199/book_sentiment_analysis/tree/main/book_sentiment_analysis/book_spider/spider/spiders)中代理和cookie的使用

## Usage

```shell
flask run
```

现在打开浏览器，输入 http://localhost:5000 并按下 Enter 即可访问主页

## Reference

[ruia](https://github.com/howie6879/ruia)

[watchlist](https://github.com/greyli/watchlist)

##  License

[MIT](https://choosealicense.com/licenses/mit/)

