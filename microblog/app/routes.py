from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, NewPostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from datetime import datetime
from sqlalchemy import desc, asc


def get_next_page_or(default):
    next_page = request.args.get('next')
    urls_valid = ('index', 'logout', 'login', 'register')
    if next_page and next_page in urls_valid and url_for(next_page).netloc == "":
        return next_page
    return url_for(default)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(get_next_page_or('index'))
    return render_template('login.html', title='Sign In', form=form)


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
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    post = Post.query.filter_by(user_id=current_user.id).order_by(desc(Post.timestamp)).first()
    return render_template('index.html', title='Home', post=post)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.username != username:
        flash('You do not have permission to view this page')
        return redirect(url_for('index'))
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New post created successfully.')
        return redirect(url_for('user', username=current_user.username))
    return render_template('new_post.html', title='New Post', form=form)
