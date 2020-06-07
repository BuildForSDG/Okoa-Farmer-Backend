from src.models.item import ItemModel
from src.models.item_category import ItemCategoryModel
from src.models.user import UserModel
from tests.test_base import TestBase


class TestItemIntegration(TestBase):
    def test_item_integration(self):
        with self.app_context():
            # 'itemname', 'userid', 'categoryid', 'location', 'cost', 'status','description', 'photo_path'
            user =UserModel('username','firstname', 'lastname', 'residence', 'address', 'phonenumber', 'emailaddress','password')
            item_category = ItemCategoryModel('categoryname')
            item = ItemModel('itemname', '1', '1', 'location', '100', '4',
                                                'description', 'photo_path')

            self.assertIsNone(item.find_by_itemname('itemname','1'))
            self.assertIsNone(item.find_by_id(1))
            user.save_to_db()
            item_category.save_to_db()
            item.save_to_db()

            self.assertIsNotNone(item.find_by_itemname('itemname','1'))
            self.assertIsNotNone(item.find_by_id(1))
