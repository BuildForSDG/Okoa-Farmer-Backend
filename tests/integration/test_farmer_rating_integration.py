from src.models.farmer_rating import FarmerRatingModel
from src.models.item import ItemModel
from src.models.item_category import ItemCategoryModel
from src.models.user import UserModel
from tests.test_base import TestBase


class TestFarmerRatingIntegration(TestBase):
    def test_role_integration(self):
        with self.app_context():

            user =UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password')
            user2 =UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password')
            item_category = ItemCategoryModel('categoryname')
            item = ItemModel('itemname', '1', '1', 'location', '100', '4',
                                                'description', 'photo_path')
            # 'farmerid','itemid','ratedby','rating'
            farmer_rating = FarmerRatingModel('1', '1', '2', '1')

            self.assertIsNone(farmer_rating.find_by_farmerid('1', '1', '2'))
            self.assertIsNone(farmer_rating.find_by_id(1))
            user.save_to_db()
            user2.save_to_db()
            item_category.save_to_db()
            item.save_to_db()
            farmer_rating.save_to_db()

            self.assertIsNotNone(farmer_rating.find_by_farmerid('1', '1', '2'))
            self.assertIsNotNone(farmer_rating.find_by_id(1))
