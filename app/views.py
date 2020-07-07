from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy import or_

from app import db
from app.models import User, Dog


class DogsApi(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    @staticmethod
    def get_owner(owner):
        user = User.query.filter_by(username=owner).first()
        return user

    def get_arguments(self):
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('breed', type=str)
        self.parser.add_argument('age', type=int)
        self.parser.add_argument('description', type=str, required=False)
        self.parser.add_argument('owner', type=str)
        return self.parser.parse_args()

    def get_id(self):
        self.parser.add_argument('dog_id', type=int, help='Wrong type id')
        arg = self.parser.parse_args()
        return arg['dog_id']

    @jwt_required
    def get(self):
        try:
            dog_id = self.get_id()
            raw_dog = Dog.query.outerjoin(User, User.id == Dog.owner_id)\
                .add_columns(User.username)\
                .filter(Dog.id == dog_id)\
                .first()
            if not raw_dog:
                return Response(status=204)
            dog = raw_dog[0].to_dict()
            dog['owner'] = raw_dog[1]
            return dog, 200
        except Exception as e:
            raise e

    @jwt_required
    def post(self):
        try:
            args = self.get_arguments()
            args['owner'] = self.get_owner(args['owner'])
            if not all(args.values()):
                return Response(status=400)
            new_dog = Dog(**args)
            db.session.add(new_dog)
            db.session.commit()
            return new_dog.id, 201
        except Exception as e:
            raise e

    @jwt_required
    def put(self):
        try:
            # print(self.__dir__())
            args = self.get_arguments()
            dog_id = self.get_id()
            dog = Dog.query.get(dog_id)
            if not dog:
                return Response(status=204)
            user = self.get_owner(args['owner'])
            dog.name = args["name"] if args["name"] is not None else dog.name
            dog.breed = args["breed"] if args["breed"] is not None else dog.breed
            dog.age = args["age"] if args["age"] is not None else dog.age
            dog.description = args["description"] if args["description"] is not None else dog.description
            dog.owner_id = user.id if args["owner"] is not None else dog.owner_id
            db.session.commit()
            return Response(status=201)
        except Exception as e:
            raise e

    @jwt_required
    def delete(self):
        try:
            dog_id = self.get_id()
            dog = Dog.query.get(dog_id)
            if not dog:
                return Response(status=204)
            db.session.delete(dog)
            db.session.commit()
            return Response(status=200)
        except Exception as e:
            raise e


class DogsListApi(Resource):
    # get all
    @jwt_required
    def get(self):
        try:
            all_dogs = Dog.query.filter_by(active=True).order_by(Dog.name).all()
            result = [dog.to_dict() for dog in all_dogs]
            return result, 200
        except Exception as e:
            raise e

    # get filtered (OR)
    @jwt_required
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('breed', type=str)
            parser.add_argument('age', type=int)
            args = parser.parse_args()
            if not any(args.values()):
                return Response(status=400)
            dogs = Dog.query.filter(or_(Dog.name == args['name'], Dog.breed == args['breed'],
                                        Dog.age == args['age'])).all()
            if not dogs:
                return Response(status=204)
            result = [dog.to_dict() for dog in dogs]
            return result, 200
        except Exception as e:
            raise e


class UserDogsApi(Resource):
    # get all user's dogs
    @jwt_required
    def get(self, user_id):
        try:
            all_dogs = Dog.query.outerjoin(User, User.id == user_id) \
                .add_columns(User.username) \
                .filter(Dog.owner_id == user_id) \
                .all()
            if not all_dogs:
                return Response(status=204)
            dogs = [dog[0].to_dict() for dog in all_dogs]
            return {'user': all_dogs[0][1], 'dogs': dogs}, 200
        except Exception as e:
            raise e


class StartApi(Resource):
    def get(self):
        try:
            return {'message': 'hello, FLASK'}, 200
        except Exception as e:
            raise e
