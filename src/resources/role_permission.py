from flask import jsonify
from flask_jwt import jwt_required
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


    # @jwt_required()
    def post(self):
        data = RolePermissionRegister.parser.parse_args()

        if RolePermissionModel.find_by_id(data['id']):
            return {'message': 'A role permission with that id already exists'}, 400
        user = RolePermissionModel(**data)
        user.save_to_db()
        return {'message': 'Role Permission created successfully.'}, 201

    @jwt_required()
    def put(self, id):
        data = RolePermissionRegister.parser.parse_args()
        role = RolePermissionModel.find_by_name(id)
        if role is None:
            role = RolePermissionModel(id, **data)
        else:
            role.roleid = data['roleid']
            role.permissionid = data['permissionid']
        role.save_to_db()
        return role.json()

    # @jwt_required()
    def get(self):
        permissions = RolePermissionModel.query.all()
        result = []

        for permission in permissions:
            role_permission_data = {}
            role_permission_data['roleid'] = permission.roleid
            role_permission_data['permissionid'] = permission.permissionid


            result.append(role_permission_data)

        return jsonify({'permissions': result})


    def delete(self, id):
        role_permission = RolePermissionModel.find_by_id(id)
        if role_permission:
            role_permission.delete_from_db()

        return jsonify({'message': 'Role Permission Deleted'})
