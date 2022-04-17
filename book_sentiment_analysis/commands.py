"""
 General commands
 Created by janeho at 14/03/2022.
"""
import click
from book_sentiment_analysis import app, db
from book_sentiment_analysis.models import Book


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def init_db(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    books = [
        {'sku': '27891166', 'category_path': '01.03.56.03.00.00',
         'img': 'https://img3m6.ddimg.cn/94/11/27891166-1_b_9.jpg',
         'book_name': '老人与海（精装版，收录《老人与海》《乞力马扎罗的雪》等）', 'author': '(美)海明威著；张炽恒译', 'publisher': '时代文艺出版社',
         'publication_date': '2019-07-01', 'price': '17.40', 'score': '90', 'reviews_count': '37214',
         'url': 'https://product.dangdang.com/27891166.html'},
        {'sku': '25087565', 'category_path': '01.43.77.01.00.00',
         'img': 'https://img3m5.ddimg.cn/74/11/25087565-1_b_18.jpg',
         'book_name': '老人与海(青少版。诺贝尔文学奖得主海明威代表作之一，详细注释版）', 'author': '美］欧内斯特・海明威 著 张姗 译', 'publisher': '浙江工商大学出版社',
         'publication_date': '2017-06-01', 'price': '18.40', 'score': '90', 'reviews_count': '46420',
         'url': 'https://product.dangdang.com/25087565.html'},
        {'sku': '24183943', 'category_path': '01.03.56.03.00.00',
         'img': 'https://img3m3.ddimg.cn/25/3/24183943-1_b_215.jpg',
         'book_name': '作家榜经典：老人与海（全新未删节插图精装版！海明威作品！人可以被毁灭，但不能被打败！读经典名著，认准作家榜！）',
         'author': '[美] 海明威 著，作家榜经典 出品，鲁羊（诗人作家） 译，大星文化，Slava Shults 绘，', 'publisher': '浙江文艺出版社',
         'publication_date': '2017-02-20', 'price': '16.90', 'score': '100', 'reviews_count': '282139',
         'url': 'https://product.dangdang.com/24183943.html'},
        {'sku': '29240762', 'category_path': '01.43.77.02.00.00',
         'img': 'https://img3m2.ddimg.cn/23/32/29240762-1_b_11.jpg', 'book_name': '老人与海（中小学生课外阅读指导丛书）无障碍阅读 彩插励志版',
         'author': '(美)海明威，', 'publisher': '南方出版社', 'publication_date': '2021-05-01', 'price': '13.40', 'score': '100',
         'reviews_count': '234353', 'url': 'https://product.dangdang.com/29240762.html'},
        {'sku': '25267184', 'category_path': '01.43.77.01.00.00',
         'img': 'https://img3m4.ddimg.cn/8/32/25267184-1_b_5.jpg', 'book_name': '老人与海（《语文》阅读丛书）人民文学出版社',
         'author': '（美国）欧内斯特・海明威', 'publisher': '人民文学出版社', 'publication_date': '2018-04-01', 'price': '17.80',
         'score': '90', 'reviews_count': '52195', 'url': 'https://product.dangdang.com/25267184.html'}
    ]
    for book in books:
        book = Book(sku=book['sku'], img=book['img'], book_name=book['book_name'], author=book['author'],
                    publisher=book['publisher'], publication_date=book['publication_date'], price=book['price'],
                    score=book['score'], reviews_count=book['reviews_count'], url=book['url'])
        db.session.add(book)

    db.session.commit()
    click.echo('Done.')
