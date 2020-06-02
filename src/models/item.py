from sqlalchemy.orm import relationship, backref

from src.models.Model import db
from src.models.item_category import ItemCategoryModel


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(80))
    userid = db.Column(db.Integer)
    categoryid = db.Column(db.Integer,db.ForeignKey('item_categories.id'))
    location = db.Column(db.String(80))
    cost = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)
    description = db.Column(db.String(200))
    photo_path = db.Column(db.String(100))


    item_category = relationship(ItemCategoryModel, backref=backref("items", cascade="all, delete-orphan"))
    # photo = db.Column(db.LargeBinary)

    def __init__(self,itemname, userid, categoryid, location, cost, status, description, photo_path):
        self.itemname = itemname
        self.userid = userid
        self.categoryid = categoryid
        self.location = location
        self.cost = cost
        self.status = status
        self.description = description
        self.photo_path = photo_path

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_itemname(cls, itemname):
        return cls.query.filter_by(itemname=itemname).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
