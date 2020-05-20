import json

from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from werkzeug.security import generate_password_hash

from src.models.user import UserModel


class UserRegister(Resource):
    """
    This resource allows users to register by sending a
    POST request with their username and password.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('residence', type=str)
    parser.add_argument('address', type=str)
    parser.add_argument('phonenumber', type=str)
    parser.add_argument('emailaddress', type=str)

    # @jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()
        data['password'] = generate_password_hash(data['password'], method='sha256')

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully.'}, 201

    @jwt_required()
    def put(self, name):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_name(name)
        if user is None:
            user = UserModel(name, **data)
        else:
            user.username = data['username']
        user.save_to_db()
        return user.json()

    # @jwt_required()
    def get(self):
        users = UserModel.query.all()
        result = []

        for user in users:
            user_data = {}
            user_data['username'] = user.username
            user_data['firstname'] = user.firstname
            user_data['lastname'] = user.lastname
            user_data['residence'] = user.residence
            user_data['address'] = user.address
            user_data['phonenumber'] = user.phonenumber
            user_data['emailaddress'] = user.emailaddress
            user_data['password'] = user.password

            result.append(user_data)

        return jsonify({'users': result})
