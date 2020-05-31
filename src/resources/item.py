import bcrypt
from flask import jsonify
from flask_jwt_extended import *
from flask_restful import Resource, reqparse
from sqlalchemy import LargeBinary

from src.models.item import ItemModel


class ItemRegister(Resource):
    """
    This resource allows itmes to be registered by sending a
    POST request with itemname, userid, categoryid, location, cost, status, photo, description and password.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('itemname',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('userid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('categoryid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('location',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('cost', type=int)
    parser.add_argument('status', type=int)
    # parser.add_argument('photo', type=LargeBinary)
    parser.add_argument('description', type=str)
    parser.add_argument('photo_path', type=str)

    @jwt_required
    def post(self):
        data = ItemRegister.parser.parse_args()
        if ItemModel.find_by_itemname(data['itemname']):
            return {'message': 'An Item with that name already exists'}, 400
        item = ItemModel(**data)
        item.save_to_db()
        return {'message': 'Item created successfully.'}, 201

    @jwt_required
    def put(self, name):
        data = ItemRegister.parser.parse_args()
        item = ItemModel.find_by_itemname(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.itemname = data['itemname']
        item.save_to_db()
        return item.json()

    @jwt_required
    def get(self):
        items = ItemModel.query.all()
        result = []

        for item in items:
            _data = {}
            _data['itemname'] = item.itemname
            _data['userid'] = item.userid
            _data['categoryid'] = item.categoryid
            _data['location'] = item.location
            _data['cost'] = item.cost
            _data['status'] = item.status
            _data['description'] = item.description
            _data['photo_path'] = item.photo_path

            result.append(_data)

        return jsonify({'items': result})


# filter item by given id
class ItemFilter(Resource):

    @jwt_required
    def delete(self,id):
        items = ItemModel.find_by_id(id)
        if items:
            items.delete_from_db()
            return jsonify({'message': 'Item Deleted'})

        return jsonify({'message': 'Item not Found'})

    @jwt_required
    def get(self,id):
        items = ItemModel.find_by_id(id)
        if items:
            _data = {}
            _data['itemname'] = items.itemname
            _data['userid'] = items.userid
            _data['categoryid'] = items.categoryid
            _data['location'] = items.location
            _data['cost'] = items.cost
            _data['status'] = items.status
            _data['description'] = items.description
            _data['photo_path'] = items.photo_path
            return jsonify({'items': _data})

        return jsonify({'message': 'Item not Found'})
