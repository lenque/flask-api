from app import api
from .auth import SignupApi, LoginApi
from .views import DogsApi, DogsListApi, StartApi

api.add_resource(StartApi, '/')
api.add_resource(SignupApi, '/api/auth/signup')
api.add_resource(LoginApi, '/api/auth/login')
api.add_resource(DogsApi, '/api/dogs')

api.add_resource(DogsListApi, '/api/dogslist')


# from app import app
# from flask import Blueprint, jsonify
# from app.models import User, Dog
# dogs_bp = Blueprint('dogs', __name__)
#
#
# @dogs_bp.route('/dogs')
# def get_ds():
#     all_dogs = Dog.query.all()
#     return jsonify({u.id: u.name for u in all_dogs})

# app.register_blueprint(dogs_bp)

# @app.route('/dogs')
# def get_ds():
#     all_dogs = Dog.query.all()
#     return jsonify({u.id: u.name for u in all_dogs})



