import bcrypt
from flask_jwt_extended import create_access_token

from src.models.user import UserModel
from tests.base_test import BaseTest
import json
from src.app import app

user_dict = {'username': 'username', 'firstname': 'firstname', 'lastname': 'lastname',
             'residence': 'residence', 'address': 'address',
             'phonenumber': 'phonenumber', 'emailaddress': 'emailaddress',
             'password': 'password'}


class UserTest(BaseTest):

    def setUp(self):
        super(UserTest, self).setUp()
        with app.test_client() as client:
            with self.app_context():
                UserModel('username', 'firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress',
                          'password').save_to_db()
                username = 'username'
                password = 'password'
                access_token = create_access_token(identity={"username": username})
                self.access_token = {"access_token": access_token}, 200

    def test_get_user_not_found(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/register', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def rest_register_and_login(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/register', data=user_dict)
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_register_duplicate_user(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/register', data=user_dict)
                response = client.post('/register', data=user_dict)

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'}, json.loads(response.data))

    # def test_delete_user(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             client.post('/register', data=user_dict)
    #             resp = client.delete('/register/username')
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertDictEqual({'message': 'User Deleted'},
    #                                  json.loads(resp.data))
