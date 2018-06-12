from app import app, db
from app.models import User, Post
from flask_mail import Message
from app import mail


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Post': Post,
            'mail': mail,
            'Message': Message
            }
