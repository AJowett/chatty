import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY') or 'secret key'
  MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
  MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['True','true', 'on', '1']
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_SUBJECT_PREFIX = '[CHATTY]'
  MAIL_SENDER = 'Chatty Admin <chatty@example.com>'
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

config = {
  'development': DevelopmentConfig,
  'default': DevelopmentConfig
}
