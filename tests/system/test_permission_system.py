import bcrypt
from flask_jwt_extended import create_access_token

from src.models.user import UserModel
from src.models.permission import PermissionModel
from tests.test_base import TestBase
import json
from src.app import app

permissions_dict = {id:'1','name': 'name'}


class TestUserSystem(TestBase):

    def setUp(self):
        super(TestUserSystem, self).setUp()
        with app.test_client() as client:
            with self.app_context():
                UserModel('username', 'firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress',
                          'password').save_to_db()
                username = 'username'
                password = 'password'
                access_token = create_access_token(identity={"username": username,password: 'password'})
                self.access_token = {"access_token": access_token}, 200

    # def test_get_permission_not_found(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             resp = client.get('/permissions',data=permissions_dict, headers={'Authorization': self.access_token})
    #             self.assertEqual(resp.status_code, 200)

    # def test_register_duplicate_permission(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             client.post('/permissions', data=permissions_dict)
    #             response = client.post('/permissions', data=permissions_dict)
    #
    #             self.assertEqual(response.status_code, 400)
    #             self.assertDictEqual({'message': 'Permission with that name already exists'}, json.loads(response.data))

    # def test_delete_permission(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             client.post('/permissions', data=permissions_dict)
    #             resp = client.delete('/permissions')
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertDictEqual({'message': 'Permission Deleted'},
    #                                  json.loads(resp.data))
