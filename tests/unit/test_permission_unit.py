from src.models.permission import PermissionModel
from tests.unit.test_base_unit import TestBaseUnit

class TestPermissionUnit(TestBaseUnit):
    def test_add_permission_unit(self):
        permission =PermissionModel('name')
        self.assertEqual(permission.name, 'name',"permissions do not match")
