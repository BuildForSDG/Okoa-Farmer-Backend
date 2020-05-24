import bcrypt
from flask_jwt_extended import create_access_token

from src.models.user import UserModel
from src.models.role import RoleModel
from tests.test_base import TestBase
import json
from src.app import app

permissions_dict = {'name': 'name'}


class TestRoleSystem(TestBase):

    def setUp(self):
        super(TestRoleSystem, self).setUp()
        with app.test_client() as client:
            with self.app_context():
                UserModel('username', 'firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress',
                          'password').save_to_db()
                username = 'username'
                access_token = create_access_token(identity={"username": username})
                self.access_token = {"access_token": access_token}, 200

    def test_get_permission_not_found(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/roles/name', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)

    def test_register_duplicate_permission(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/roles/name', data=permissions_dict)
                response = client.post('/roles/name', data=permissions_dict)

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A role with that name already exists'}, json.loads(response.data))

    def test_delete_permission(self):
        with app.test_client() as client:
            with self.app_context():
                client.post('/roles/name', data=permissions_dict)
                resp = client.delete('/roles/name')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Role Deleted'},
                                     json.loads(resp.data))
