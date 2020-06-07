import json

from flask_jwt_extended import create_access_token

from app import app
from src.models.permission import PermissionModel
from src.models.role import RoleModel
from src.models.user import UserModel
from tests.test_base import TestBase

user_dict = {"username": "testusername", 'password': 'testpassword'}
_role = {'name': 'admin'}
_permission = {'name': 'add'}
role_permission_dict = {'roleid': '1', 'permissionid': '1'}


class TestUserSystem(TestBase):
    # initial setup to register user, use credentials to get access token
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

    # test if role permission exists or not
    def test_get_role_permission_not_found(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/role/permissions/1/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 400)

    # test registering an already existing permission
    def test_duplicate_role_permission(self):
        with app.test_client() as client:
            with self.app_context():
                RoleModel('admin').save_to_db()
                PermissionModel('add').save_to_db()
                client.post('/role/permissions', data=role_permission_dict,
                            headers={'Authorization': self.access_token})
                response = client.post('/role/permissions', data=role_permission_dict,
                                       headers={'Authorization': self.access_token})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A role with that permission already exists'},
                                     json.loads(response.data))

    # get role permission given roleid and permissionid
    def test_get_single_user(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/role/permissions/1/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 400)

    # test delete role permission given roleid and permissionid
    def test_delete_role_permission(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/role/permissions/1/1', data=user_dict, headers={'Authorization': self.access_token})
                resp = client.delete('/role/permissions/1/1', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Role Permission Not Found'},
                                     json.loads(resp.data))
