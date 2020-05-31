from src.models.farmer_rating import FarmerRatingModel
from tests.test_base import TestBase


class TestFarmerRatingIntegration(TestBase):
    def test_role_integration(self):
        with self.app_context():
            # 'farmerid','itemid','ratedby','rating'
            farmer_rating = FarmerRatingModel('1', '2', '3', '4')

            self.assertIsNone(farmer_rating.find_by_farmerid('1', '2', '3'))
            self.assertIsNone(farmer_rating.find_by_id(1))

            farmer_rating.save_to_db()

            self.assertIsNotNone(farmer_rating.find_by_farmerid('1', '2', '3'))
            self.assertIsNotNone(farmer_rating.find_by_id(1))
