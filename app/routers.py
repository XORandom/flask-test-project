from flask import render_template
from app import app


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
