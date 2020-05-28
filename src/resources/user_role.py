from flask import jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from src.models.user_role import UserRoleModel


class UserRoleRegister(Resource):
    """
    This resource allows user role to be registered by sending a
    POST request with their userole and roleid.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('userid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('roleid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")

    # @jwt_required()
    def post(self):
        data = UserRoleRegister.parser.parse_args()
        if UserRoleModel.find_by_id(data['userid'], data['roleid']):
            return {'message': 'A user with that role already exists'}, 400
        user_role = UserRoleModel(**data)
        user_role.save_to_db()
        return {'message': 'User Role created successfully.'}, 201

    @jwt_required()
    def put(self, id):
        data = UserRoleRegister.parser.parse_args()
        user_role = UserRoleModel.find_by_id(id)
        if user_role is None:
            user_role = UserRoleModel(id, **data)
        else:
            user_role.userid = data['userid']
            user_role.roleid = data['roleid']
        user_role.save_to_db()
        return user_role.json()

    # @jwt_required()
    def get(self):
        data = UserRoleRegister.parser.parse_args()
        user = UserRoleModel.find_by_id(data['userid'], data['roleid'])

        user_role_data = {}
        user_role_data['userid'] = user.userid
        user_role_data['roleid'] = user.roleid

        return jsonify({'user_roles': user_role_data})


    def delete(self, id):
        user_role = UserRoleModel.find_by_id(id)
        if user_role:
            user_role.delete_from_db()

        return jsonify({'message': 'User Role Deleted'})


# get all user roles
class UserRoleGet(Resource):

    # @jwt_required()
    def get(self):
        user_role = UserRoleModel.query.all()
        result = []

        for user in user_role:
            user_role_data = {}
            user_role_data['userid'] = user.userid
            user_role_data['roleid'] = user.roleid

            result.append(user_role_data)

        return jsonify({'user_role_data': result})
