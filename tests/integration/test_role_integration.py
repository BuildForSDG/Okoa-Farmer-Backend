from src.models.role import RoleModel
from tests.test_base import TestBase


class TestRoleIntegration(TestBase):
    def test_role_integration(self):
        with self.app_context():
            role = RoleModel('name')
            self.assertIsNone(role.find_by_name('name'))
            self.assertIsNone(role.find_by_id(1))
            role.save_to_db()
            self.assertIsNotNone(role.find_by_name('name'))
            self.assertIsNotNone(role.find_by_id(1))
