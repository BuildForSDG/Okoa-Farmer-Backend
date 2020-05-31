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
            return jsonify({'message': 'An Item Category with that name already exists'}, 400)
        item_categories = ItemCategoryModel(**data)
        item_categories.save_to_db()
        return jsonify({'message': 'Item Category created successfully.'}, 201)

    @jwt_required
    def get(self):
        item_categories = ItemCategoryModel.query.all()
        result = []

        for item_category in item_categories:
            role_data = {}
            role_data['categoryname'] = item_category.categoryname
            result.append(role_data)

        return jsonify({'roles': result})

    @jwt_required
    def put(self, categoryname):
        data = ItemCategoryRegister.parser.parse_args()
        item_categories = ItemCategoryModel.find_by_categoryname(categoryname)
        if item_categories is None:
            item_categories = ItemCategoryModel(categoryname, **data)
        else:
            item_categories.categoryname = data['categoryname']
        item_categories.save_to_db()
        return item_categories.json()


# filter Role by given id
class ItemCategoryFilter(Resource):

    @jwt_required
    def delete(self, id):
        # item_categories = ItemCategoryModel.find_by_id(id)
        item_categories = ItemCategoryModel.find_by_categoryname(id)
        if item_categories:
            item_categories.delete_from_db()
            return jsonify({'message': 'Item Category Deleted'})
        return jsonify({'message': 'Item Category not Found'})

    @jwt_required
    def get(self, id):
        item_categories = ItemCategoryModel.find_by_categoryname(id)
        if item_categories:
            _data = {}
            _data['id'] = item_categories.id
            _data['categoryname'] = item_categories.categoryname

            return jsonify({'item_categoriess': _data})

        return jsonify({'message': 'Item Category not Found'})
