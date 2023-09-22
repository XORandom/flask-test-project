from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlparse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/index')
@login_required
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
    return render_template('index.html', title='Дом', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user=user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)
