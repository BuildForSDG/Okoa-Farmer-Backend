from src.models.user_role import UserRoleModel
from src.models.role import RoleModel
from src.models.user import UserModel
from tests.test_base import TestBase


class TestRolePermissionIntegration(TestBase):
    def test_user_role_integration(self):
        with self.app_context():
            role= RoleModel('admin')
            user =UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password')

            self.assertIsNone(role.find_by_name('admin'))
            self.assertIsNone(user.find_by_username('username'))

            user_role = UserRoleModel('1', '1')
            self.assertIsNone(user_role.findby_id(1))
            role.save_to_db()
            user.save_to_db()
            user_role.save_to_db()
            self.assertIsNotNone(user_role.findby_id(1))
            self.assertIsNotNone(user_role.findby_id(1))

