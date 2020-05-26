from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import  create_access_token, create_refresh_token
from models.users import UserModel
import sqlite3

_parser = reqparse.RequestParser()
_parser.add_argument('username',
                     type=str,
                     required=True,
                     help="Username field cannot be left blank!!"
    )
_parser.add_argument('password',
                     type=str,
                     required=True,
                     help="Password field cannot be left blank!!"
    )
_parser.add_argument('email',
                     type=str,
                     required=False,
                     store_missing=True,
                     help="Email field cannot be left blank"

    )

class UserRegister(Resource):
    def post(self):
        data = _parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message":"{} : username is allready taken".format(data['username'])}, 400
        elif data['email'] is None:
            return {"message":"YOU must add Email!"}, 400
        try:
            user = UserModel(**data)
            user.save_to_db()
        except:
            return {"message":"UUps something went wrong"}, 500

        return {"message":"User created successfully"}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':"User ({}) not found".format(user_id)}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message':"User ({}) not found".format(user_id)}, 404
        user.delete_from_db()
        return {'message': "User ({}) sucsessfuly deleted".format(user_id)},200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _parser.parse_args()


        user = UserModel.find_by_username(data['username'])


        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id , fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message':'Invalid credentials'}, 401

