from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


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
