from src.models.user import UserModel
from tests.base_test import BaseTest

class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user =UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password')

            self.assertIsNone(UserModel.find_by_username('username'))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username('username'))
            self.assertIsNotNone(UserModel.find_by_id(1))
