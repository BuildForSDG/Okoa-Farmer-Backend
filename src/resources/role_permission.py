from flask import jsonify
from flask_jwt_extended import *
from flask_restful import Resource, reqparse

from src.models.role_permission import RolePermissionModel


class RolePermissionRegister(Resource):
    """
    This resource allows role_permission to be registered by sending a
    POST request with their roleid and permissionid.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('roleid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('permissionid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")

    @jwt_required
    def post(self):
        data = RolePermissionRegister.parser.parse_args()
        if RolePermissionModel.find_by_id(data['roleid'], data['permissionid']):
            return {'message': 'A role with that permission already exists'}, 400
        user = RolePermissionModel(**data)
        user.save_to_db()
        return {'message': 'Role Permission created successfully.'}, 201

    @jwt_required
    def get(self):
        permissions = RolePermissionModel.query.all()
        result = []

        for permission in permissions:
            role_permission_data = {}
            role_permission_data['permissionid'] = permission.permissionid
            role_permission_data['roleid'] = permission.roleid

            result.append(role_permission_data)

        return jsonify({'role_permissions': result})


# filter Role Permission by given id
class RolePermissionFilter(Resource):

    @jwt_required
    def delete(self, roleid, permissionid):
        role_permission = RolePermissionModel.find_by_id(roleid, permissionid)
        if role_permission:
            role_permission.delete_from_db()
            return jsonify({'message': 'Role Permission Deleted'})
        return jsonify({'message': 'Role Permission Not Found'})

    @jwt_required
    def get(self, roleid, permissionid):
        role_permission = RolePermissionModel.find_by_id(roleid, permissionid)
        if role_permission:
            _data = {}
            _data['id'] = role_permission.id
            _data['roleid'] = role_permission.roleid
            _data['permissionid'] = role_permission.permissionid
            return jsonify({'users': _data})

        return jsonify({'message': 'Role Permission not Found'})

    @jwt_required
    def put(self, roleid, permissionid):
        data = RolePermissionRegister.parser.parse_args()
        role_permission = RolePermissionModel.find_by_id(roleid, permissionid)
        if role_permission:
            role_permission.roleid = data['roleid']
            role_permission.permissionid = data['permissionid']
            role_permission.save_to_db()
            return jsonify({'message': 'Role Permission updated successfully'})
        return jsonify({'message': 'Role Permission not Found'})
