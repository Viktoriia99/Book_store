from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, DecimalField, FileField, TextAreaField, SubmitField, SelectField, IntegerField, \
    PasswordField
from wtforms.validators import InputRequired, Length, NumberRange


class BookForm(FlaskForm):
    name = StringField(
        'Назва книги',
        render_kw={'placeholder': 'Майстер та Маргарита'},
        validators=[
            InputRequired(),
            Length(min=1, max=64, message='Назва не має бути довшою за 64 символи')
            ]
        )
    author = StringField(
        'Автор',
        validators=[InputRequired()],
        description='бажано у форматі Прізвище І.П. (наприклад, Булгаков. М.О.)',
        render_kw={'placeholder': 'Булгаков М.О.'}
        )
    genre = SelectField(
        'Жанр',
        choices=[
            ('Роман', 'Роман'),
            ('В', 'Поезія'),
            ('Драма', 'Драма')
        ]
    )
    amount = IntegerField(
        'Кіл-ть екземплярів',
        default=0,
        validators=[
            NumberRange(min=0, message='Число має бути додатнім')
        ],
    )
    year = IntegerField(
        'Рік видавництва',
        default=0,
        validators=[
            NumberRange(min=0, message='Число має бути додатнім')
        ],
    )
    price = DecimalField(
        'Ціна екземпляру',
        render_kw={'placeholder': '17.49'},
        validators=[
            InputRequired(),
            NumberRange(min=0.01, message='Ціна має бути додатнім числом')
            ]
        )
    image = FileField(
        'Зовраження обкладинки',
        validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Лише jpg и png!')],
        )
    description = TextAreaField(
        'Опис книги',
        render_kw={'placeholder': '«Ма́йстер та Маргари́та» — роман Михайла Опанасовича Булгакова, робота над яким розпочалася наприкінці 1920-х років і тривала аж до смерті письменника. Роман належить до незавершених творів; редагування та зведення докупи чорнових записів здійснювала після смерті чоловіка вдова письменника — Олена Сергіївна.'}
        )
    publisher = TextAreaField(
        'Видавництво'
    )
    submit = SubmitField('Ок')


class LoginForm(FlaskForm):
    username = StringField(
        "Им'я користувача",
        validators=[
            InputRequired(),
        ]
    )
    password = PasswordField(
        'Пароль',
        validators=[
            InputRequired(),
        ]
    )
    submit = SubmitField('Увійти')
