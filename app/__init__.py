from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config


app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)


from app import routes, models


# db = SQLAlchemy()
# migrate = Migrate()
#
#
# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)
#     from .models import db
#     db.init_app(app)
#     migrate = Migrate()
#     migrate.init_app(app, db)
#     return app



# CREATE DATABASE flask_db;
# CREATE USER flaskuser WITH PASSWORD 'password';
# ALTER ROLE flaskuser SET client_encoding TO 'utf8';
# ALTER ROLE flaskuser SET default_transaction_isolation TO 'read committed';
# ALTER ROLE flaskuser SET timezone TO 'UTC';
# GRANT ALL PRIVILEGES ON DATABASE flask_db TO flaskuser;
