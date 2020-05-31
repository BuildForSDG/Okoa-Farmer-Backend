from src.models.item_category import ItemCategoryModel
from tests.unit.test_base_unit import TestBaseUnit

class TestItemCategoryUnit(TestBaseUnit):
    def test_item_category_unit(self):
        item_category = ItemCategoryModel('categoryname')
        self.assertEqual(item_category.categoryname, 'categoryname', "names do not match")
