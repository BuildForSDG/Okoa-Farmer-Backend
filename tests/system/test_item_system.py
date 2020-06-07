import json

from flask_jwt_extended import create_access_token

from app import app
from src.models.item_category import ItemCategoryModel
from src.models.user import UserModel
from tests.test_base import TestBase

# 'itemname', 'userid', 'categoryid', 'location', 'cost', 'status','description', 'photo_path'
item_dict = {'itemname': 'itemname', 'userid': '1', 'categoryid': '1',
             'location': 'location', 'cost': '20',
             'status': '1', 'description': 'description',
             'photo_path': 'photo_path'}
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

    # get item information
    def test_get_item(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/item', data=item_dict, headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    # try to register an item twice
    def test_register_duplicate_item(self):
        with app.test_client() as client:
            with self.app_context():
                ItemCategoryModel('categoryname').save_to_db()
                client.post('/item', data=item_dict, headers={'Authorization': self.access_token})
                response = client.post('/item', data=item_dict, headers={'Authorization': self.access_token})
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'An Item with that name already exists'}, json.loads(response.data))

    # test to delete item
    def test_delete_item(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/item', data=item_dict)
                resp = client.delete('/item/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
                # self.assertDictEqual({'message': 'Item Deleted'},
                #                      json.loads(resp.data))
