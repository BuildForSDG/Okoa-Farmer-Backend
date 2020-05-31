from src.models.Model import db


class ItemCategoryModel(db.Model):
    __tablename__ = 'item_categories'

    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(80))


    def __init__(self, categoryname):
        self.categoryname = categoryname

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_categoryname(cls, categoryname):
        return cls.query.filter_by(categoryname=categoryname).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
