from src.models.role_permission import RolePermissionModel
from src.models.role import RoleModel
from src.models.permission import PermissionModel
from tests.test_base import TestBase


class TestRolePermissionIntegration(TestBase):
    def test_role_permission_integration(self):
        with self.app_context():
            _role = RoleModel('admin')
            _permission = PermissionModel('dashboard')
            role_permission = RolePermissionModel('1', '1')
            _role.save_to_db()
            _permission.save_to_db()
            role_permission.save_to_db()
            self.assertIsNotNone(role_permission.findby_id(1))
