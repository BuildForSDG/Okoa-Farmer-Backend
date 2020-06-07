import json

from flask_jwt_extended import create_access_token

from app import app
from src.models.role import RoleModel
from src.models.user import UserModel
from tests.test_base import TestBase

user_dict = {"username": "testusername", 'password': 'testpassword'}
role_dict = {'name': 'admin'}
user_role_dict = {'userid': '1', 'roleid': '1'}


class TestUserSystem(TestBase):

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

    def test_get_user_not_found(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/user/roles/1/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
    #
    def test_register_duplicate_user(self):
        with app.test_client() as client:
            with self.app_context():
                UserModel('testuser', 'firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','testpassword').save_to_db()
                RoleModel('admin').save_to_db()
                client.post('/user/roles', data=user_role_dict, headers={'Authorization': self.access_token})
                response = client.post('/user/roles', data=user_role_dict, headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that role already exists'}, json.loads(response.data))

    def test_get_single_user(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/user/roles/1/1', data=user_dict, headers={'Authorization': self.access_token})
                resp = client.get('/user/roles/1/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def test_delete_user(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/user/roles/1/1', data=user_dict, headers={'Authorization': self.access_token})
                resp = client.delete('/user/roles/1/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'User Role not Found'},
                                     json.loads(resp.data))
