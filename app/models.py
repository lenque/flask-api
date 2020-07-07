from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    dogs = db.relationship('Dog', backref='owner', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    @staticmethod
    def set_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, username, email, password, admin=False, active=True):
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.active = active
        
    def __repr__(self):
        return f'User {self.username}'


class Dog(db.Model):
    __tablename__ = 'dogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        res = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and key != "active":
                res[key] = value
        return res

    def __repr__(self):
        return f"Dog {self.name}"


# MIGRATIONS
# flask db init   # initialize Alembic, create new folder called “migrations”
# flask db migrate   # create migration (no changes to the db)
# flask db migrate -m "users table"   # create specific migration
# flask db upgrade   # apply changes to the db

# PYTHON SHELL
# >>> from app import db
# >>> from app.models import User, Dog
# >>> u = User(username="Igor", email="Igor@gmail.com", password='password')
# >>> db.session.add(u)
# >>> d = Dog(name="Monetka", breed="nobreed", age=2, owner=u, description="good girl")
# >>> db.session.add(d)
# >>> db.session.commit()

# SNAP=true /snap/postman/current/usr/share/Postman/Postman
