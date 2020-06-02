from sqlalchemy.orm import relationship, backref

from src.models.Model import db
from src.models.item_category import ItemCategoryModel
from src.models.user import UserModel


class FarmerRatingModel(db.Model):
    __tablename__ = 'farmer_rating'

    id = db.Column(db.Integer, primary_key=True)
    farmerid = db.Column(db.Integer)
    itemid = db.Column(db.Integer)
    ratedby = db.Column(db.Intege) #userid
    rating = db.Column(db.Integer)

    # id = db.Column(db.Integer, primary_key=True)
    # farmerid = db.Column(db.Integer,db.ForeignKey('users.id'))
    # itemid = db.Column(db.Integer,db.ForeignKey('item_categories.id'))
    # ratedby = db.Column(db.Integer,db.ForeignKey('users.id')) #userid
    # rating = db.Column(db.Integer)

    # user = relationship(UserModel, backref=backref("farmer_rating", cascade="all, delete-orphan"))
    # item_category = relationship(ItemCategoryModel, backref=backref("farmer_rating", cascade="all, delete-orphan"))
    #

    def __init__(self,farmerid,itemid,ratedby,rating):
        self.farmerid = farmerid
        self.itemid = itemid
        self.ratedby = ratedby
        self.rating = rating

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_farmerid(cls, farmerid,itemid,ratedby):
        return cls.query.filter_by(farmerid=farmerid,itemid=itemid,ratedby=ratedby).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
