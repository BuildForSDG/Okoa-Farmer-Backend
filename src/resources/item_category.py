from flask import jsonify
from flask_jwt_extended import *
from flask_restful import Resource, reqparse

from src.models.item_category import ItemCategoryModel


class ItemCategoryRegister(Resource):
    """
    This resource allows roles registration by sending a
    POST request with the categoryname.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('categoryname',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    @jwt_required
    def post(self):
        data = ItemCategoryRegister.parser.parse_args()
        if ItemCategoryModel.find_by_categoryname(data['categoryname']):
            return {'message': 'An Item Category with that name already exists'}, 400
        item_categories = ItemCategoryModel(**data)
        item_categories.save_to_db()
        return {'message': 'Item Category created successfully.'}, 200

    @jwt_required
    def get(self):
        item_categories = ItemCategoryModel.query.all()
        result = []

        for item_category in item_categories:
            role_data = {}
            role_data['categoryname'] = item_category.categoryname
            result.append(role_data)

        return {'roles': result, 'message':'successful transaction'}, 200


# filter Role by given id
class ItemCategoryFilter(Resource):

    @jwt_required
    def delete(self, categoryname):
        # item_categories = ItemCategoryModel.find_by_id(id)
        item_categories = ItemCategoryModel.find_by_categoryname(categoryname)
        if item_categories:
            item_categories.delete_from_db()
            return jsonify({'message': 'Item Category Deleted'})
        return jsonify({'message': 'Item Category not Found'})

    @jwt_required
    def get(self, categoryname):
        item_categories = ItemCategoryModel.find_by_categoryname(categoryname)
        if item_categories:
            _data = {}
            _data['id'] = item_categories.id
            _data['categoryname'] = item_categories.categoryname

            return {'item_categoriess': _data}, 200

        return {'message': 'Item Category not Found'}, 400

    @jwt_required
    def put(self, categoryname):
        data = ItemCategoryRegister.parser.parse_args()
        item_categories = ItemCategoryModel.find_by_categoryname(categoryname)
        if item_categories:
            item_categories.categoryname = data['categoryname']
            item_categories.save_to_db()
            return {'message': 'Category name updated successfully'}, 200
        ItemCategoryModel(categoryname, **data)
        return {'message': 'Category name not Found'}, 400
