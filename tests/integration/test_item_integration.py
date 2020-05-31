from src.models.item import ItemModel
from tests.test_base import TestBase


class TestItemIntegration(TestBase):
    def test_item_integration(self):
        with self.app_context():
            # 'itemname', 'userid', 'categoryid', 'location', 'cost', 'status','description', 'photo_path'
            item = ItemModel('itemname', '2', '3', 'location', '100', '4',
                                                'description', 'photo_path')

            self.assertIsNone(item.find_by_itemname('itemname'))
            self.assertIsNone(item.find_by_id(1))

            item.save_to_db()

            self.assertIsNotNone(item.find_by_itemname('itemname'))
            self.assertIsNotNone(item.find_by_id(1))
