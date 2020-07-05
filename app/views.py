from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from app import db
from app.models import User, Dog


class DogsApi(Resource):
    @jwt_required
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('dog_id', type=int, location='args', help='Wrong type id')
            args = parser.parse_args()
            raw_dog = Dog.query.join(User, Dog.owner_id == User.id)\
                .add_columns(User.username)\
                .filter_by(id=args['dog_id']).first()
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
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('breed', type=str)
            parser.add_argument('age', type=int)
            parser.add_argument('description', type=str, required=False)
            parser.add_argument('owner', type=str)
            args = parser.parse_args()
            args['owner'] = User.query.filter_by(username=args['owner']).first()
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
            parser = reqparse.RequestParser()
            parser.add_argument('dog_id', type=int, location='args', help='Wrong type id')
            parser.add_argument('name', type=str)
            parser.add_argument('breed', type=str)
            parser.add_argument('age', type=int)
            parser.add_argument('description')
            parser.add_argument('owner', type=str)
            args = parser.parse_args()
            dog = Dog.query.get(args['dog_id'])
            if not dog:
                return Response(status=204)
            user = User.query.filter_by(username=args['owner']).first()
            dog.name = args["name"] if args["name"] is not None else dog.name
            dog.breed = args["breed"] if args["breed"] is not None else dog.breed
            dog.age = args["age"] if args["age"] is not None else dog.age
            dog.description = args["description"] if args["description"] is not None else dog.description
            dog.owner_id = user.id if args["owner"] is not None else dog.owner_id
            db.session.add(dog)
            db.session.commit()
            return Response(status=201)
        except Exception as e:
            raise e


class DogsListApi(Resource):
    @jwt_required
    def get(self):
        try:
            all_dogs = Dog.query.order_by(Dog.name).all()
            return {u.id: u.name for u in all_dogs}, 200
        except Exception as e:
            raise e


class StartApi(Resource):
    def get(self):
        try:
            return {'message': 'hello, FLASK'}, 200
        except Exception as e:
            raise e
