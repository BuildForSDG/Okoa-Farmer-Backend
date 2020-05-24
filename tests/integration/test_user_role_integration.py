from src.models.user_role import UserRoleModel
from tests.test_base import TestBase


class TestRolePermissionIntegration(TestBase):
    def test_role_permission_integration(self):
        with self.app_context():
            user_role = UserRoleModel('1', '6')
            self.assertIsNone(user_role.find_by_id(1))
            user_role.save_to_db()
            self.assertIsNotNone(user_role.find_by_id(1))
