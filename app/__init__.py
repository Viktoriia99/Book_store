import pickle
from flask import Flask, send_from_directory
from flask_bootstrap import Bootstrap5
from book import Book
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap5(app)

with open('all_books.bin', 'rb') as file:
    all_books = pickle.load(file)
    Book.max_id = len(all_books)

from app.controllers import home_controller
from app.controllers import book_controller

@app.route('/icon.png')
def icon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'icon.png', mimetype='image/png')




