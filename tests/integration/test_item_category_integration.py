from src.models.item_category import ItemCategoryModel
from tests.test_base import TestBase


class TestItemCategoryIntegration(TestBase):
    def test_item_integration(self):
        with self.app_context():
            role = ItemCategoryModel('categoryname')

            self.assertIsNone(role.find_by_categoryname('categoryname'))
            self.assertIsNone(role.find_by_id(1))

            role.save_to_db()

            self.assertIsNotNone(role.find_by_categoryname('categoryname'))
            self.assertIsNotNone(role.find_by_id(1))


