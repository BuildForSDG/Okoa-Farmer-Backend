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


# filter user by given id
class UserFilter(Resource):

    @jwt_required
    def delete(self,id):
        user = UserModel.find_by_id(id)
        if user:
            user.delete_from_db()
            return jsonify({'message': 'User Deleted'})

        return jsonify({'message': 'User not Found'})

    @jwt_required
    def get(self,id):
        user = UserModel.find_by_id(id)
        if user:
            _data = {}
            _data['username'] = user.username
            _data['firstname'] = user.firstname
            _data['lastname'] = user.lastname
            _data['residence'] = user.residence
            _data['address'] = user.address
            _data['phonenumber'] = user.phonenumber
            _data['emailaddress'] = user.emailaddress
            return jsonify({'users': _data})

        return jsonify({'message': 'User not Found'})

    @jwt_required
    def put(self, id):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(id)
        if user:
            user.username = user.username
            user.firstname = data['firstname']
            user.lastname= data['lastname']
            user.residence = data['residence']
            user.address = data['address']
            user.phonenumber = data['phonenumber']
            user.emailaddress= data['emailaddress']
            user.save_to_db()
            return jsonify({'message': 'User updated successfully'})
        return jsonify({'message': 'User not Found'})

