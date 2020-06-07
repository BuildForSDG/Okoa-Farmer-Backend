import json

from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import *

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

    @jwt_required
    def post(self):
        data = PermissionRegister.parser.parse_args()
        if PermissionModel.find_by_name(data['name']):
            return {'message': 'Permission with that name already exists'}, 400
        permission = PermissionModel(**data)
        permission.save_to_db()
        return {'message': 'Permission created successfully.'}, 201

    @jwt_required
    def get(self):
        permissions = PermissionModel.query.all()
        result = []

        for permission in permissions:
            _data = {}
            _data['id'] = permission.id
            _data['name'] = permission.name
            result.append(_data)

        return jsonify({'permissions': result})


# filter permissions by given id
class PermissionFilter(Resource):

    @jwt_required
    def delete(self, name):
        permission = PermissionModel.find_by_name(name)
        if permission:
            permission.delete_from_db()
            return jsonify({'message': 'Permission Deleted'})
        return jsonify({'message': 'Permission not Found'})

    @jwt_required
    def get(self, name):
        permission = PermissionModel.find_by_name(name)
        if permission:
            _data = {}
            _data['id'] = permission.id
            _data['name'] = permission.name
            return jsonify({'permissions': _data})
        return jsonify({'message': 'Permission not Found'})

    @jwt_required
    def put(self, name):
        data = PermissionRegister.parser.parse_args()
        permission = PermissionModel.find_by_name(name)
        if permission:
            permission.name = data['name']
            permission.save_to_db()
            return jsonify({'message': 'permission updated successfully'})
        # permission = PermissionModel(id, **data)
        return jsonify({'message': 'permission not Found'})
