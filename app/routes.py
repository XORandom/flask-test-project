from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'XORandom'}
    posts = [
        {
            'author': {'username': 'Наташа'},
            'sex': 'Female',
            'body': 'Хочется домой...'
        },
        {
            'author': {'username': 'Андрей'},
            'sex': 'Male',
            'body': 'Да пора уже'
        }
    ]
    return render_template('index.html', title='Work', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.remember_me.data:

            flash(f'Ваш логин {form.username.data}, '
                  f'запомнил вас')
        else:
            flash(f'Ваш логин {form.username.data}, '
                  f'не запомнил вас')
        return redirect('/index')
    return render_template('login.html', title='Вход', form=form)

