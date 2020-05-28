import bcrypt
from flask import jsonify
from flask_jwt_extended import *
from flask_restful import Resource, reqparse

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
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        # data['password'] = generate_password_hash(data['password'], method='sha256')

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully.'}, 201

    @jwt_required
    def put(self, name):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_name(name)
        if user is None:
            user = UserModel(name, **data)
        else:
            user.username = data['username']
        user.save_to_db()
        return user.json()

    @jwt_required
    def get(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        _data = {}
        _data['username'] = user.username
        _data['firstname'] = user.firstname
        _data['lastname'] = user.lastname
        _data['residence'] = user.residence
        _data['address'] = user.address
        _data['phonenumber'] = user.phonenumber
        _data['emailaddress'] = user.emailaddress

        return jsonify({'users': _data})

    @jwt_required
    def delete(self, name):
        user = UserModel.find_by_username(name)
        if user:
            user.delete_from_db()

        return jsonify({'message': 'User Deleted'})


# get all users
class UserGet(Resource):

    @jwt_required
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
