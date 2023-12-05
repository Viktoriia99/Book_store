from flask import url_for


class Book:
    max_id = 0

    def __init__(self, name, author, price, genre, amount=0, description='', filename=''):
        self.id = Book.max_id
        self.name = name
        self.author = author
        self.price = price
        self.genre = genre
        self.amount = amount
        self.description = description
        self.filename = filename
        Book.max_id += 1

    @property
    def cover(self):
        filename = f'img/cover_{self.filename}' if self.filename else f'img/default_book_cover.jpg'
        return url_for('static', filename=filename)

    def __str__(self):
        return f'<Book {self.id}: {self.name}>'
