# [DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://flaskuser:password@172.17.0.1:5432/flask_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'somesecretkey'
    PROPAGATE_EXCEPTIONS = True
