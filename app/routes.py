from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required, login_manager
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from app.models import User
# from werkzeug.urls import url_parse
from urllib.parse import urlparse
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Наташа'},
            'gender': 'F',
            'body': 'Хочется домой...'
        },
        {
            'author': {'username': 'Андрей'},
            'gender': 'M',
            'body': 'Да пора уже'
        }
    ]
    return render_template('index.html', title='Флудилка', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_login = User.query.filter_by(username=form.username.data).first()
        if user_login is None or not user_login.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль ')
            return redirect(url_for('login'))
        login_user(user=user_login, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
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
        # user = User(username=form.username.data, email=form.email.data)
        user_new = User()
        user_new.set_gender(form.gender.data)
        user_new.set_username(form.username.data)
        user_new.set_email(form.email.data)
        user_new.set_password(form.password.data)
        db.session.add(user_new)
        db.session.commit()
        flash('Регистрация прошла успешно')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Редактирование профиля',
                           form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user_ = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user_, 'body': "Пора домой!!!"},
        {'author': user_, 'body': "Скорее уже!!!"}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user_, posts=posts, form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash(f'Пользователь {username} не найден')
            return redirect(url_for('index'))
        if user == current_user:
            flash(f'Нельзя подписаться на самого себя')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()  # Добавляем связь в БД
        flash(f'Вы подписались на {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        # if user is None:
        #     flash(f'Пользователь {username} не найден')
        #     return redirect(url_for('index'))
        # if user == current_user:
        #     flash(f'Нельзя отписаться от самого себя')
        #     return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()  # Добавляем связь в БД
        flash(f'Вы отписались от {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
