from app import app, all_books
import pandas as pd
from flask import render_template, url_for, flash, make_response, request, abort
import os
import pickle
from app.forms.forms import BookForm
from book import Book
from werkzeug.utils import secure_filename, redirect


books1 = pd.read_csv('data2/Books.csv', sep=',', on_bad_lines='skip', encoding="latin-1", low_memory=False)
books1.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher','imageUrlS', 'imageUrlM', 'imageUrlL', 'price', 'count']

@app.route('/books')
@app.route('/books/')
@app.route('/catalog')
@app.route('/catalog/')
@app.route('/books/index')
@app.route('/books/index/')
def books():
    # пагінаці (показ обмеженої кількості елементів на сторінці
    # з можливістю переглядати інші за допомогою кнопок навігації)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    books2 = books1[start:end]
    total_pages = len(books1) // per_page + (1 if len(books1) % per_page else 0)

    # last_viewing_book_id = request.cookies.get('book_id')
    # last_viewing_book = all_books.get(int(last_viewing_book_id)))
    last_viewing_books_id = request.cookies.get('books_id')
    last_viewing_books = []
    '''if last_viewing_books_id:
        books_id = last_viewing_books_id[:-1].split(',')
        print(books_id)
        for book_id in books_id:
            if all_books.get(int(book_id)):
                last_viewing_books.append(all_books.get(int(book_id)))
            print(last_viewing_books)
    '''
    return render_template('books/index.html', page=page, total_pages=total_pages, books=books2.to_dict('records'), bookss=all_books, title='Книги', last_viewing_books=last_viewing_books,
                           #last_viewing_book=last_viewing_book
                           )


@app.route('/books/<string:id>')
@app.route('/books/<string:id>/')
def book(id):
    b = books1.loc[books1['ISBN'] == id]

    # Перевірка, чи DataFrame порожній
    if b.empty:
        return abort(404)
    b = b.iloc[0]
    res = make_response(render_template(f'books/book.html', book=b, title=f"{b['bookTitle']} - {b['bookAuthor']}"))
    last_viewing_books_id = request.cookies.get('books_id')
    if not last_viewing_books_id:
        last_viewing_books_id = ''
    else:
        books_id = last_viewing_books_id[:-1].split(',')
        if len(books_id) > 2:
            last_viewing_books_id = ','.join(books_id[1:]) + ','
        if str(id) in books_id:
            print(id, books_id, last_viewing_books_id)
            books_id.remove(str(id))
            last_viewing_books_id = ','.join(books_id) + ','

    last_viewing_books_id += str(id) + ','
    res.set_cookie('books_id', last_viewing_books_id)
    # res.set_cookie('book_id', str(id))
    return res


@app.route('/books/create', methods=['GET', 'POST'])
@app.route('/books/create/', methods=['GET', 'POST'])
# @ensure_logged_in
def create_book():
    form = BookForm()
    if form.validate_on_submit():
        img_dir = os.path.join(os.path.dirname(app.instance_path), 'app\static', 'img')
        f = form.image.data
        filename = ''
        if f:
            print(f)
            filename = secure_filename(f.filename)
            f.save(os.path.join(img_dir, 'cover_' + filename))

        new_book = Book(name=form.name.data, author=form.author.data, price=float(round(form.price.data, 2)),
                        genre=form.genre.data, amount=form.amount.data, description=form.description.data,
                        filename=filename)
        all_books[new_book.id] = new_book
        with open('../all_books.bin', 'wb') as file:
            pickle.dump(all_books, file)
        flash('Книга успішно додана.', 'success')
        return redirect(url_for('create_book'))
    return render_template('books/book_form.html', form=form, action_name='Створення', book='')


@app.route('/books/<string:id>/edit', methods=['GET', 'POST'])
@app.route('/books/<string:id>/edit/', methods=['GET', 'POST'])
# @ensure_logged_in
def edit_book(id):
    form = BookForm()

    editable_book = books1.loc[books1['ISBN'] == id]

    # Перевірка, чи DataFrame порожній
    if editable_book.empty:
        return abort(404)
    editable_book = editable_book.iloc[0]

    if form.validate_on_submit():
        img_dir = books1.loc[books1['imageUrlS'] == id]
        f = form.image.data
        '''filename = secure_filename(f.filename)
        if filename and filename != editable_book.filename:
            f.save(os.path.join(img_dir, 'cover_' + filename))

            old_file = os.path.join(img_dir, 'cover_' + editable_book.filename)
            editable_book.filename = filename
            if os.path.exists(old_file):
                os.remove(old_file)
        '''

        editable_book.loc[books['ISBN'] == id, 'bookTitle'] = form.name.data
        editable_book.loc[books['ISBN'] == id, 'bookAuthor'] = form.author.data
        editable_book.loc[books['ISBN'] == id, 'publisher'] = form.publisher.data
        editable_book.loc[books['ISBN'] == id, 'count'] = form.amount.data
        editable_book.loc[books['ISBN'] == id, 'yearOfPublication'] = form.year.data
        # editable_book.genre = form.genre.data
        editable_book.loc[books['ISBN'] == id, 'price'] = float(round(form.price.data, 2))
        # editable_book.description = form.description.data

        '''with open('../all_books.bin', 'wb') as file:
            pickle.dump(all_books, file)'''
        flash('Книга успішно відредагована.', 'success')
        return redirect(url_for('book', id=editable_book['ISBN']))

    form.name.data = editable_book['bookTitle']
    # form.genre.data = editable_book['bookTitle']
    form.image = editable_book['imageUrlS']
    # form.description.data = editable_book['bookTitle']
    form.price.data = editable_book['price']
    form.author.data = editable_book['bookAuthor']
    form.amount.data = editable_book['count']
    form.publisher.data = editable_book['publisher']
    form.year.data = editable_book['yearOfPublication']

    return render_template('books/book_form.html', form=form,
                           action_name='Редагування', book=editable_book, book_id=id)
# file=editable_book.cover,

@app.route('/books/<string:id>/remove', methods=['GET', 'POST'])
@app.route('/books/<string:id>/remove/', methods=['GET', 'POST'])
# @ensure_logged_in
def remove_book(id):
    removable_book = books1.loc[books1['ISBN'] == id]

    # Перевірка, чи DataFrame порожній
    if removable_book.empty:
        return abort(404)
    removable_book = removable_book.iloc[0]


    if request.method == 'POST':
        '''img_dir = os.path.join(os.path.dirname(app.instance_path), '../static', 'img')
        old_file = os.path.join(img_dir, 'cover_' + removable_book.filename)
        if os.path.exists(old_file):
            os.remove(old_file)
        del all_books[id]
        with open('../all_books.bin', 'wb') as file:
            pickle.dump(all_books, file)'''
        books2 = books1.drop(books1[books1['ISBN'] == id].index)
        flash('Книга успішно видалена.', 'success')
        book1 = books2
        return redirect(url_for('books'))

    return render_template('books/remove_book.html', book=removable_book)