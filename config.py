import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
#local
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Masaki2017$$@localhost/okoa_farmer_db"

#server
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://b2b1802e9376f5:91ac6855@us-cdbr-east-06.cleardb.net/okoa_farmer_db?charset=utf8mb4"

#travis
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:''@localhost/okoa_farmer_db"
