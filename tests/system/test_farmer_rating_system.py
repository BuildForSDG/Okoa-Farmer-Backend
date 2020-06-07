import json

from flask_jwt_extended import create_access_token

from app import app
from src.models.item import ItemModel
from src.models.item_category import ItemCategoryModel
from src.models.user import UserModel
from tests.test_base import TestBase

# 'farmerid','itemid','ratedby','rating'
farmer_rating_dict = {'farmerid':'1', 'itemid':'1', 'ratedby':'1', 'rating':'1'}
user_logins = {'username': 'username', 'password': 'password'}


class TestUserSystem(TestBase):

    # initial setup to register user, use registered credentials to get access token
    def setUp(self):
        super(TestUserSystem, self).setUp()
        with app.test_client() as client:
            with self.app_context():
                UserModel('username', 'firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress',
                          'password').save_to_db()
                username = 'username'
                password = 'password'
                access_token = create_access_token(identity={"username": username, "password": password})
                auth_token = access_token
                self.access_token = f' Bearer {auth_token}'

    # get farmer_rating information
    def test_get_farmer_rating(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/farmer/rating', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    # try to register a farmer_rating twice
    def test_register_duplicate_farmer_rating(self):
        with app.test_client() as client:
            with self.app_context():
                ItemCategoryModel('categoryname').save_to_db()
                UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password').save_to_db()
                ItemModel('itemname', '1', '1', 'location', '100', '1',
                                                'description', 'photo_path').save_to_db()

                client.post('/farmer/rating', data=farmer_rating_dict, headers={'Authorization': self.access_token})
                response = client.post('/farmer/rating', data=farmer_rating_dict,
                                       headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Farmer Item Rating by that user already exists'},
                                     json.loads(response.data))

    # test to delete farmer_rating
    def test_delete_farmer_rating(self):
        with app.test_client() as client:
            with self.app_context():
                ItemCategoryModel('categoryname').save_to_db()
                UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password').save_to_db()
                ItemModel('itemname', '1', '1', 'location', '100', '1',
                                                'description', 'photo_path').save_to_db()
                client.post('/farmer/rating', data=farmer_rating_dict, headers={'Authorization': self.access_token})
                resp = client.delete('/farmer/rating/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Farmer Item Rating Deleted'},
                                     json.loads(resp.data))
