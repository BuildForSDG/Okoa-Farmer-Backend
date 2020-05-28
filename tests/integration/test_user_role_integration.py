# from src.models.user_role import UserRoleModel
# from src.models.role import RoleModel
# from src.models.user import UserModel
# from tests.test_base import TestBase
#
#
# class TestRolePermissionIntegration(TestBase):
#     def test_role_permission_integration(self):
#         with self.app_context():
#             RoleModel('admin')
#             UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password')
#             user_role = UserRoleModel('1', '1')
#             self.assertIsNone(user_role.findby_id(1))
#             user_role.save_to_db()
#             self.assertIsNotNone(user_role.findby_id(1))
