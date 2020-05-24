from src.models.Model import db


class UserRoleModel(db.Model):
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    roleid = db.Column(db.Integer)

    def __init__(self, userid, roleid):
        self.userid = userid
        self.roleid = roleid

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
