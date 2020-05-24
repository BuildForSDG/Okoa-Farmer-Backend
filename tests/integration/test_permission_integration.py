from src.models.permission import PermissionModel
from tests.test_base import TestBase

class TestPermissionIntegration(TestBase):
    def test_user_integration(self):
        with self.app_context():
            permission =PermissionModel('name')

            self.assertIsNone(permission.find_by_name('name'))
            self.assertIsNone(permission.find_by_id(1))

            permission.save_to_db()

            self.assertIsNotNone(permission.find_by_name('name'))
            self.assertIsNotNone(permission.find_by_id(1))
