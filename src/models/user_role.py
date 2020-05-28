from sqlalchemy.orm import relationship, backref

from src.models.Model import db
from src.models.user import UserModel
from src.models.role import RoleModel


class UserRoleModel(db.Model):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    roleid = db.Column(db.Integer, db.ForeignKey('roles.id'))

    user = relationship(UserModel, backref=backref("user_roles", cascade="all, delete-orphan"))
    role = relationship(RoleModel, backref=backref("user_roles", cascade="all, delete-orphan"))

    def __init__(self, userid, roleid):
        self.userid = userid
        self.roleid = roleid

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def findby_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_id(cls, userid,roleid):
        return cls.query.filter_by(userid=userid,roleid=roleid).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
