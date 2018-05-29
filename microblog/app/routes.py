from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sergio'}
    posts = [
        {
            'author': {'username': 'Robe'},
            'body': 'Mira que camiseta mas chula!'
        },
        {
            'author': {'username': 'Edgar'},
            'body': 'Yo gasto la sintaxis es6'
        },
        {
            'author': {'username': 'Sergio'},
            'body': 'Se lo que me dices'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
