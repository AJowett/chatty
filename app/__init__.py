from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from flask_sock import Sock
from config import config

bootstrap = Bootstrap4()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
sock = Sock()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)

  bootstrap.init_app(app)
  mail.init_app(app)
  moment.init_app(app)
  db.init_app(app)
  login_manager.init_app(app)

  login_manager.login_view = 'auth.login'

  # Register blueprins with the application
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  from .api import api as api_blueprint
  app.register_blueprint(api_blueprint)

  from .sockets import sockets as sockets_blueprint
  app.register_blueprint(sockets_blueprint)

  sock.init_app(app)

  return app