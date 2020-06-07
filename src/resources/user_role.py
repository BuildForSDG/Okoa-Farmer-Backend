import json

from flask import jsonify
from flask_jwt_extended import *
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

    @jwt_required
    def post(self):
        data = UserRoleRegister.parser.parse_args()
        if UserRoleModel.find_by_id(data['userid'], data['roleid']):
            return {'message': 'A user with that role already exists'}, 400

        user_role = UserRoleModel(**data)
        user_role.save_to_db()
        return {'message': 'User Role created successfully.'}, 200

    @jwt_required
    def get(self):
        user_role = UserRoleModel.query.all()
        result = []

        for user in user_role:
            user_role_data = {}
            user_role_data['userid'] = user.userid
            user_role_data['roleid'] = user.roleid

            result.append(user_role_data)
        return jsonify({'user_role_data': result})

    @jwt_required
    def delete(self, id):
        user_role = UserRoleModel.find_by_id(id)
        if user_role:
            user_role.delete_from_db()

        return jsonify({'message': 'User Role Deleted'})


# # filter user roles
class UserRoleFilter(Resource):
    @jwt_required
    def delete(self, userid, roleid):
        user_role = UserRoleModel.find_by_id(userid, roleid)
        if user_role:
            user_role.delete_from_db()
            return jsonify({'message': 'User Role Deleted'})
        return jsonify({'message': 'User Role not Found'})

    @jwt_required
    def get(self, userid, roleid):
        user_role = UserRoleModel.find_by_id(userid, roleid)
        if user_role:
            _data = {}
            _data['id'] = user_role.id
            _data['userid'] = user_role.userid
            _data['roleid'] = user_role.roleid
            return jsonify({'user_roles': _data, 'message': 'successful transaction'})

        return jsonify({'message': 'User Role not Found'})


    @jwt_required
    def put(self, userid, roleid):
        data = UserRoleRegister.parser.parse_args()
        role_permission = UserRoleModel.find_by_id(userid, roleid)
        if role_permission:
            role_permission.userid = data['userid']
            role_permission.roleid = data['roleid']
            role_permission.save_to_db()
            return jsonify({'message': 'User Role updated successfully'})
        return jsonify({'message': 'User Role not Found'})

