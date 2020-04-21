import os

""" Database Settings """
BASEDIR = os.path.abspath(os.path.dirname(__file__))

""" For local database testing change the default values in each of the four environ.get calls in the format section of `SQLALCHEMY_DATABASE_URI` """
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(os.environ.get('SQLALCHEMY_DATABASE_USERNAME', 'root'),
                                                               os.environ.get('SQLALCHEMY_DATABASE_PASSWORD', 'password'),
                                                               os.environ.get('MYSQL_HOST', '192.168.1.20'),
                                                               os.environ.get('SQLALCHEMY_DATABASE_DATABASE', 'pingplotter'))
SQLALCHEMY_POOL_SIZE = int(os.environ.get('SQLALCHEMY_POOL_SIZE', '2'))
SQLALCHEMY_POOL_RECYCLE = int(os.environ.get('SQLALCHEMY_POOL_RECYCLE', '600'))
SQLALCHEMY_TRACK_MODIFICATIONS = eval(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False'))
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

""" Flask Options (ignored by Gunicorn) """
FLASK_DEBUG = True
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5151

""" Debug tokens """
TOKEN_DEBUG = True


