# flask-test-project


Удаление пользователя из БД
```cmd
flask shell
>>> user = User.query.get(1)
>>> db.session.delete(user)
>>> db.session.commit()
```
