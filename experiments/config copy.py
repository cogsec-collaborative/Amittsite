import os


basedir = os.path.abspath(os.path.dirname(__file__))


# Keys
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'


# Database setup
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'amittsite.sqlite')
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#     os.path.join(basedir, 'amittsite.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

