from src.models.role_permission import RolePermissionModel
from tests.unit.test_base_unit import TestBaseUnit


class TestRolePermissionUnit(TestBaseUnit):
    def test_user_unit(self):
        user_role = RolePermissionModel('2', '4')

        self.assertEqual(user_role.roleid, '2', "roleid do not match")
        self.assertEqual(user_role.permissionid, '4', "permissionid do not match")
