import json

from flask_jwt_extended import create_access_token

from src.app import app
from src.models.user import UserModel
from tests.test_base import TestBase

roles_dict = {'name': 'name'}


class TestRoleSystem(TestBase):

    def setUp(self):
        super(TestRoleSystem, self).setUp()
        with app.test_client() as client:
            with self.app_context():
                UserModel('username', 'firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress',
                          'password').save_to_db()
                username = 'username'
                password = 'password'
                access_token = create_access_token(identity={"username": username,password:'password'})
                self.access_token = {"access_token": access_token}, 200

    # def test_get_permission_not_found(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             resp = client.get('/roles', data=roles_dict, headers={'Authorization': self.access_token})
    #             self.assertEqual(resp.status_code, 200)

    def test_register_duplicate_permission(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/roles', data=roles_dict)
                response = client.post('/roles', data=roles_dict)

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A role with that name already exists'}, json.loads(response.data))

    # def test_delete_permission(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             client.post('/roles', data=roles_dict)
    #             resp = client.delete('/roles')
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertDictEqual({'message': 'Role Deleted'},
    #                                  json.loads(resp.data))
