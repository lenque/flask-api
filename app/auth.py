import datetime
from flask import Response
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from app import db
from app.models import User


class SignupApi(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True)
            parser.add_argument('email', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            args = parser.parse_args()
            if not all(args.values()):
                return Response(status=204)
            user = User(**args)
            db.session.add(user)
            db.session.commit()
            user_id = user.id
            return {'id': str(user_id)}, 201
        except Exception as e:
            raise e


class LoginApi(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True)
            parser.add_argument('password', type=str, required=True)
            args = parser.parse_args()
            user = User.query.filter_by(username=args['username']).first()
            if not user or not user.check_password(args['password']):
                return {'error': 'invalid credentials'}, 401
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
        except Exception as e:
            raise e
