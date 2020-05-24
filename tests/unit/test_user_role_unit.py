from src.models.user_role import UserRoleModel
from tests.unit.test_base_unit import TestBaseUnit

class TestUserRoleUnit(TestBaseUnit):
    def test_user_unit(self):

        user_role =UserRoleModel('1','3')

        self.assertEqual(user_role.userid, '1',"userid do not match")
        self.assertEqual(user_role.roleid, '3',"roleid do not match")

