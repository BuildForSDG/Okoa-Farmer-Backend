import json

from flask import jsonify, make_response
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

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully.'}, 201

    def get(self):
        users = UserModel.query.all()
        us_d = json.dumps(str(users))
        return {'message': 'data fetched successfully', 'data': us_d}, 200
