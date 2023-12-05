from app import app
from flask import render_template, url_for, flash, session
from app.forms.forms import LoginForm
from functools import wraps
from werkzeug.utils import redirect


@app.route('/')
def index():
    return render_template('home/index.html')


@app.route('/about')
@app.route('/about/')
def about():
    return render_template('home/about.html', title='О сайте')


def ensure_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not (session.get('username') and session.get('username') in app.config['SUPERUSERS'] and
                session.get('password') and session.get('password') == app.config['SUPERUSERS'][session['username']]):
            flash('Пожалуйста, для начала зарегистрируйтесь.', 'warning')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data.lower() in app.config['SUPERUSERS'] \
                and form.password.data.lower() == app.config['SUPERUSERS'][form.username.data.lower()]:
            session['username'] = form.username.data.lower()
            session['password'] = form.password.data.lower()
            flash("Вы успешно вошли!", "success")
            return redirect(url_for('index'))
        flash('Неверные данные. Пожалуйста, попробуйте ещё раз.', 'danger')
    return render_template('home/login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    flash('Вы успешно вышли.', 'success')
    return redirect(url_for('login'))

