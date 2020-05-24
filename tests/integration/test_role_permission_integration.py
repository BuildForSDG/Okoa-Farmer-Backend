from src.models.role_permission import RolePermissionModel
from tests.test_base import TestBase


class TestRolePermissionIntegration(TestBase):
    def test_role_permission_integration(self):
        with self.app_context():
            role_permission = RolePermissionModel('1', '6')
            self.assertIsNone(role_permission.find_by_id(1))
            role_permission.save_to_db()
            self.assertIsNotNone(role_permission.find_by_id(1))
