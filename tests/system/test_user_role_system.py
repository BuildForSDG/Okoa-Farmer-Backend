from flask_jwt_extended import create_access_token

from src.app import app
from src.models.user import UserModel
from tests.test_base import TestBase

user_dict = {'id': '2',"username":"testusername", 'password': 'testpassword'}
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
                access_token = create_access_token(identity={"username": username,"password": password})
                self.access_token = {"access_token": access_token}, 200

    # def test_get_user_not_found(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             resp = client.get('/user/roles/id', headers={'Authorization': self.access_token})
    #             self.assertEqual(resp.status_code, 200)
    #
    # def test_register_duplicate_user(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             UserModel('testuser', 'firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','testpassword').save_to_db()
    #             RoleModel('admin').save_to_db()
    #             client.post('/user/roles/idname', data=user_role_dict)
    #             response = client.post('/user/roles/idname', data=user_role_dict)
    #
    #             self.assertEqual(response.status_code, 400)
    #             self.assertDictEqual({'message': 'A user role with that id already exists'}, json.loads(response.data))
    #
    # def test_delete_user(self):
    #     with app.test_client() as client:
    #         with self.app_context():
    #             client.post('/register/username', data=user_dict)
    #             resp = client.delete('/register/username')
    #             self.assertEqual(resp.status_code, 200)
    #             self.assertDictEqual({'message': 'User Deleted'},
    #                                  json.loads(resp.data))
