import json

from flask_jwt_extended import create_access_token

from app import app
from src.models.user import UserModel
from tests.test_base import TestBase

user_dict = {'username': 'username', 'firstname': 'firstname', 'lastname': 'lastname',
             'residence': 'residence', 'address': 'address',
             'phonenumber': 'phonenumber', 'emailaddress': 'emailaddress',
             'password': 'password'}
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

    # get user information
    def test_get_user(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/api/register', data=user_dict, headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    # try to register a user twice
    def test_register_duplicate_user(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/api/register', data=user_dict)
                response = client.post('/register', data=user_dict)
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'}, json.loads(response.data))

    # test to delete user
    def test_delete_user(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/api/register', data=user_dict)
                resp = client.delete('/api/register/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'User Deleted'},
                                     json.loads(resp.data))
