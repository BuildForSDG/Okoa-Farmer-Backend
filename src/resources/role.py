import bcrypt
from flask import jsonify
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from src.models.role import RoleModel


class RoleRegister(Resource):
    """
    This resource allows roles registration by sending a
    POST request with the name.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    @jwt_required
    def post(self):
        data = RoleRegister.parser.parse_args()

        if RoleModel.find_by_name(data['name']):
            return {'message': 'A role with that name already exists'}, 400
        user = RoleModel(**data)
        user.save_to_db()
        return {'message': 'Role created successfully.'}, 201

    @jwt_required
    def put(self, name):
        data = RoleRegister.parser.parse_args()
        role = RoleModel.find_by_name(name)
        if role is None:
            role = RoleModel(name, **data)
        else:
            role.name = data['name']
        role.save_to_db()
        return role.json()

    @jwt_required
    def get(self):
        data = RoleRegister.parser.parse_args()
        role = RoleModel.find_by_name(data['name'])
        # role = RoleModel.find_by_id(data['id'])

        _data = {}
        _data['id'] = role.id
        _data['name'] = role.name

        return jsonify({'roles': _data})

    @jwt_required
    def delete(self, name):
        role = RoleModel.find_by_name(name)
        if role:
            role.delete_from_db()

        return jsonify({'message': 'Role Deleted'})


# get all user roles
class RoleGet(Resource):

    @jwt_required
    def get(self):
        role = RoleModel.query.all()
        result = []

        for user in role:
            role_data = {}
            role_data['name'] = user.name
            result.append(role_data)

        return jsonify({'roles': result})
