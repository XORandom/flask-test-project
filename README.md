# flask-test-project

# Создание базы данных
```cmd
flask db init 
flask db migrate -m 'user and post'
flask db upgrade
```
# Удаление пользователя из БД
```cmd
flask shell
>>> user = User.query.get(1)
>>> db.session.delete(user)
>>> db.session.commit()


flask db migrate -m 'new columns in user'
flask db upgrade
```

# Для работы с почтой
```
pip install flask_mail
```
# Генерация ключа восстановления пароля
```
pip install pyjwt 
```
