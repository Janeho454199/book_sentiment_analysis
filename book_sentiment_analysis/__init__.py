"""
 Init flask
 Created by janeho at 14/03/2022.
"""
import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),
                                                              os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'

db = SQLAlchemy(app)

from book_sentiment_analysis import views, errors, commands
