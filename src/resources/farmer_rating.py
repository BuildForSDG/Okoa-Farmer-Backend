from flask import jsonify
from flask_jwt_extended import *
from flask_restful import Resource, reqparse

from src.models.farmer_rating import FarmerRatingModel
from src.models.user import UserModel


class FarmerRatingRegister(Resource):
    """
    This resource allows roles registration by sending a
    POST request with the name.
    """

    parser = reqparse.RequestParser()
    parser.add_argument('farmerid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('itemid',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('ratedby',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('rating',
                        type=int,
                        required=True,
                        help="This field cannot be blank.")

    @jwt_required
    def post(self):
        data = FarmerRatingRegister.parser.parse_args()
        user = UserModel.query.filter_by(id=data['ratedby']).first()
        if user:
            if FarmerRatingModel.find_by_farmerid(data['farmerid'], data['itemid'], data['ratedby']):
                return {'message': 'Farmer Item Rating by that user already exists'}, 200
            farmer_r = FarmerRatingModel(**data)
            farmer_r.save_to_db()
            return {'message': 'Item rating created successfully.'}, 200
        return {'message': 'You are not registered.Kindly register to rate the farmer'}, 400

    @jwt_required
    def get(self):
        role = FarmerRatingModel.query.all()
        result = []

        for farmer_r in role:
            _data = {}
            _data['id'] = farmer_r.id
            _data['farmerid'] = farmer_r.farmerid
            _data['itemid'] = farmer_r.itemid
            _data['ratedby'] = farmer_r.ratedby
            _data['rating'] = farmer_r.rating
            result.append(_data)

        return {'roles': result, 'message': 'successful transaction'}, 200


# filter farmer rating by given farmerid, itemid, ratedby
class FarmerRatingFilter(Resource):

    @jwt_required
    def delete(self, farmerid, itemid, ratedby):
        farmer_rating = FarmerRatingModel.find_by_farmerid(farmerid, itemid, ratedby)
        if farmer_rating:
            farmer_rating.delete_from_db()
            return jsonify({'message': 'Farmer Item Rating Deleted'})
        return jsonify({'message': 'Farmer Item Rating not Found'})

    @jwt_required
    def get(self, farmerid, itemid, ratedby):
        farmer_rating = FarmerRatingModel.find_by_farmerid(farmerid, itemid, ratedby)
        if farmer_rating:
            _data = {}
            _data['id'] = farmer_rating.id
            _data['farmerid'] = farmer_rating.farmerid
            _data['itemid'] = farmer_rating.itemid
            _data['ratedby'] = farmer_rating.ratedby
            _data['rating'] = farmer_rating.rating

            return {'farmer_ratings': _data, 'message': 'successful transaction'}, 200

        return {'message': 'Farmer Item Rating not Found'}, 400

    @jwt_required
    def put(self, farmerid, itemid, ratedby):
        data = FarmerRatingRegister.parser.parse_args()
        farmer_r = FarmerRatingModel.find_by_farmerid(farmerid, itemid, ratedby)
        if farmer_r:
            farmer_r.rating = data['rating']
            farmer_r.save_to_db()
            return {'message': 'Farmer rating updated successfully'}, 200
        return {'message': 'Farmer rating not Found'}, 400


# filter farmer rating by id
class FarmerRatingIDFilter(Resource):

    @jwt_required
    def delete(self, id):
        farmer_rating = FarmerRatingModel.find_by_id(id)
        if farmer_rating:
            farmer_rating.delete_from_db()
            return jsonify({'message': 'Farmer Item Rating Deleted'})
        return jsonify({'message': 'Farmer Item Rating not Found'})

    @jwt_required
    def get(self, id):
        farmer_rating = FarmerRatingModel.find_by_id(id)
        if farmer_rating:
            _data = {}
            _data['id'] = farmer_rating.id
            _data['farmerid'] = farmer_rating.farmerid
            _data['itemid'] = farmer_rating.itemid
            _data['ratedby'] = farmer_rating.ratedby
            _data['rating'] = farmer_rating.rating

            return {'farmer_ratings': _data, 'message': 'successful transaction'}, 200

        return {'message': 'Farmer Item Rating not Found'}, 400

    @jwt_required
    def put(self, id):
        data = FarmerRatingRegister.parser.parse_args()
        farmer_r = FarmerRatingModel.find_by_id(id)
        if farmer_r:
            farmer_r.farmerid = data['farmerid']
            farmer_r.itemid = data['itemid']
            farmer_r.ratedby = data['ratedby']
            farmer_r.rating = data['rating']
            farmer_r.save_to_db()
            return {'message': 'Farmer rating updated successfully'}, 200
        return {'message': 'Farmer rating not Found'}, 400
