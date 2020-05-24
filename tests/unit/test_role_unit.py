from src.models.role import RoleModel
from tests.unit.test_base_unit import TestBaseUnit


class TestRoleUnit(TestBaseUnit):
    def test_add_role_unit(self):
        role = RoleModel('name')
        self.assertEqual(role.name, 'name', "names do not match")
