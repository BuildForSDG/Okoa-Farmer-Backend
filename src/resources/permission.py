from flask import jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from src.models.permission import PermissionModel


class PermissionRegister(Resource):
    """
    This resource allows permission registration by sending a
    POST request with the name
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    # @jwt_required()
    def post(self):
        data = PermissionRegister.parser.parse_args()

        if PermissionModel.find_by_name(data['name']):
            return {'message': 'Permission with that name already exists'}, 400
        user = PermissionModel(**data)
        user.save_to_db()
        return {'message': 'Permission created successfully.'}, 201

    @jwt_required()
    def put(self, name):
        data = PermissionModel.parser.parse_args()
        permission = PermissionModel.find_by_name(name)
        if permission is None:
            permission = PermissionModel(name, **data)
        else:
            permission.name = data['name']
        permission.save_to_db()
        return permission.json()

        # @jwt_required()

    def get(self):
        data = PermissionRegister.parser.parse_args()

        permissions= PermissionModel.find_by_name(data['name'])

        _data = {}
        _data['id'] = permissions.id
        _data['name'] = permissions.name

        return jsonify({'permissions': _data})

    def delete(self, name):
        permission = PermissionModel.find_by_name(name)
        if permission:
            permission.delete_from_db()

        return jsonify({'message': 'Permission Deleted'})


# get all permissions
class PermissionGet(Resource):

    # @jwt_required()
    def get(self):
        permissions = PermissionModel.query.all()
        result = []

        for permission in permissions:
            user_data = {}
            user_data['name'] = permission.name

            result.append(user_data)

        return jsonify({'permissions': result})
