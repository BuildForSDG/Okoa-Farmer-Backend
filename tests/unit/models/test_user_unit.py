from src.models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class TestUserUnit(UnitBaseTest):
    def test_create_user(self):
        #(self, username, firstname, lastname, residence, address, phonenumber, emailaddress, password)
        user =UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password')

        self.assertEqual(user.username, 'username',"usernames do not match")
        self.assertEqual(user.firstname, 'firstname',"firstname do not match")
        self.assertEqual(user.lastname, 'lastname',"lastname do not match")
        self.assertEqual(user.residence, 'residence',"residence do not match")
        self.assertEqual(user.address, 'address',"address do not match")
        self.assertEqual(user.phonenumber, 'phonenumber',"phonenumber do not match")
        self.assertEqual(user.emailaddress, 'emailaddress',"emailaddress do not match")
        self.assertEqual(user.password, 'password',"passwords do not match")
