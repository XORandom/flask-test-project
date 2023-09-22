# flask-test-project


Удаление пользователя из БД
```cmd
flask shell
>>> user = User.query.get(1)
>>> db.session.delete(user)
>>> db.session.commit()


flask db migrate -m 'new columns in user'
flask db upgrade
```
