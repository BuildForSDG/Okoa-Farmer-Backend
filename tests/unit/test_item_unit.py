from src.models.item import ItemModel
from tests.unit.test_base_unit import TestBaseUnit


class TestItemUnit(TestBaseUnit):
    def test_add_item_unit(self):

        item =ItemModel('itemname', 'userid', 'categoryid', 'location', 'cost', 'status', 'description', 'photo_path')

        self.assertEqual(item.itemname, 'itemname',"itemnames do not match")
        self.assertEqual(item.userid, 'userid',"userid do not match")
        self.assertEqual(item.categoryid, 'categoryid',"categoryid do not match")
        self.assertEqual(item.location, 'location',"location do not match")
        self.assertEqual(item.cost, 'cost',"cost do not match")
        self.assertEqual(item.status, 'status',"status do not match")
        self.assertEqual(item.description, 'description',"description do not match")
        self.assertEqual(item.photo_path, 'photo_path',"photo_path do not match")
        # self.assertEqual(item.photo, 'photo',"photos do not match")

