from . import db
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager
from flask import current_app, request
import hashlib
import uuid
from datetime import datetime

class Permission:
  SEND_MESSAGE = 1
  CREATE_CHANNEL = 2
  DELETE_CHANNEL = 4
  MODERATE = 8
  ADMIN = 16

class User(UserMixin, db.Model):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64), unique=True, index=True)
  username = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String(128))
  confirmed = db.Column(db.Boolean, default=False)
  avatar_hash = db.Column(db.String(32))
  messages = db.relationship('Message', backref='author', lazy='dynamic')

  @property
  def password(self):
    raise AttributeError("Password is not a readable attribute")

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

  def generate_confirmation_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'confirm': self.id}).decode('utf-8')

  def confirm(self, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
    except:
      return False

    if data.get('confirm') != self.id:
      return False
    self.confirmed = True
    db.session.add(self)
    return True

  def generate_reset_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'reset': self.id}).decode('utf-8')

  @staticmethod
  def reset_password(token, new_password):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
    except:
      return False
    user = User.query.get(data.get('reset'))
    if user is None:
      return False
    user.password = new_password
    db.session.add(user)
    return True

  def generate_email_change_token(self, email, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'change_email': self.id, 'new_email': email}).decode('utf-8')

  def change_email(self, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token.encode('utf-8'))
    except:
      return False

    if data.get('change_email') != self.id:
      return False

    new_email = data.get('new_email')
    if new_email is None:
      return False
    if self.query.filter_by(email=new_email).first() is not None:
      return False

    self.email = new_email
    self.avatar_hash = self.gravatar_hash()
    db.session.add(self)
    return True

  def gravatar_hash(self):
    return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

  def gravatar(self, size=100, default='identicon', rating='g'):
    if request.is_secure:
      url = 'https://secure.gravatar.com/avatar'
    else:
      url = 'https://www.gravatar.com/avatar'
    hash = self.avatar_hash or self.gravatar_hash()
    return f'{url}/{hash}?s={size}&d={default}&r={rating}'

class Channel(db.Model):
  __tablename__ = "channels"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  messages = db.relationship('Message', backref='channel', lazy='dynamic')

  def __repr__(self):
    return self.name

class Message(db.Model):
  __tablename__ = "messages"
  id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  body = db.Column(db.Text)
  timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))