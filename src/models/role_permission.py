from sqlalchemy.orm import relationship, backref

from src.models.Model import db
from src.models.role import RoleModel
from src.models.permission import PermissionModel


class RolePermissionModel(db.Model):
    __tablename__ = 'role_permission'

    id = db.Column(db.Integer, primary_key=True)
    roleid = db.Column(db.Integer, db.ForeignKey('roles.id'))
    permissionid = db.Column(db.Integer, db.ForeignKey('permissions.id'))


    role = relationship(RoleModel, backref=backref("role_permission", cascade="all, delete-orphan"))
    permission = relationship(PermissionModel, backref=backref("role_permission", cascade="all, delete-orphan"))


    def __init__(self, roleid, permissionid):
        self.roleid = roleid
        self.permissionid = permissionid


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, roleid,permissionid):
        return cls.query.filter_by(roleid=roleid,permissionid=permissionid).first()

    @classmethod
    def findby_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
