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
                auth_request = client.post('/auth', data=json.dumps({'username': 'username', 'password': 'password'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'  # header ={'Authorization':'JWT '+auth_token}

    def test_get_user_no_auth(self):
        with app.test_client() as client:
            with self.app_context():
                response = client.get('/register')
                self.assertEqual(response.status_code, 401)

    def test_get_user_not_found(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.get('/register', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_delete_user(self):
        with app.test_client() as client:
            with self.app_context():
                resp = client.delete('/register')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                     json.loads(resp.data))

    def test_register_user(self):
        with app.test_client() as client:
            with self.app_context():
                request = client.post('/register',
                                      data=user_dict)

                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('username'))
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(request.data))

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
