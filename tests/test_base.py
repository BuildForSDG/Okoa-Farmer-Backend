"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from src.app import app
from src.models.Model import db


class TestBase(TestCase):

    @classmethod
    def setUpClass(cls):

        #local
        # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:Masaki2017$$@localhost/okoa_farmer_db?charset=UTF8MB4"

        #server
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b2b1802e9376f5:91ac6855@us-cdbr-east-06.cleardb.net/okoa_farmer_db?charset=utf8mb4'
    
        #travis
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/okoa_farmer_db?charset=UTF8MB4'

        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # Make sure database exists
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client()
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
