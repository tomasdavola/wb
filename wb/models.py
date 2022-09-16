from wb import database, login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(25), unique=True, nullable=False)
    email = database.Column(database.String(125), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='images/default.png')
    password = database.Column(database.String(60), nullable=False)
    posts = database.relationship('Post', backref='author', lazy=True)
    date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    is_master = database.Column(database.Boolean, nullable=False, default=0)

    def get_reset_token(self, expire_time=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_time)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except KeyError:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}', '{self.date}')"


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(125), nullable=False)
    date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    content = database.Column(database.Text, nullable=False)
    author_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}','{self.date}')"

class Order(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(125), nullable=False)
    tel_num = database.Column(database.String(125), nullable=False)
    address = database.Column(database.String(200), nullable=False)
    email = database.Column(database.String(125), nullable=False)
    date = database.Column(database.DateTime, nullable=False, default=datetime.now)
    date_completed = database.Column(database.DateTime, nullable=True)
    date_i_p = database.Column(database.DateTime, nullable=True)
    order = database.Column(database.Text, nullable=False)
    file = database.Column(database.String(100), nullable=True)
    mop = database.Column(database.String(60), nullable=False,)
    is_completed = database.Column(database.Boolean, nullable=False, default=0)
    is_i_p = database.Column(database.Boolean, nullable=False, default=0)

