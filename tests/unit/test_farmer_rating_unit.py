from src.models.farmer_rating import FarmerRatingModel
from tests.unit.test_base_unit import TestBaseUnit


class TestFarmerRatingUnit(TestBaseUnit):
    def test_add_role_unit(self):
        farmer_rating = FarmerRatingModel('farmerid','itemid','ratedby','rating')
        self.assertEqual(farmer_rating.farmerid, 'farmerid', "farmerids do not match")
        self.assertEqual(farmer_rating.itemid, 'itemid', "item id's do not match")
        self.assertEqual(farmer_rating.ratedby, 'ratedby', "rated by do not match")
        self.assertEqual(farmer_rating.rating, 'rating', "ratings do not match")
