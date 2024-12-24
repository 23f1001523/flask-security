

from datetime import datetime
from flask_security import RoleMixin, UserMixin
from flask_security.models import fsqla_v3 as fsqla
from extensions import db, security

fsqla.FsModels.set_db_info(db)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='users_roles', backref='user')
    active = db.Column(db.Boolean,default=True)
    

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(50), nullable=False)

# roles_users = db.Table('roles_users',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
# )

class UserRole(db.Model):
    __tablename__ = 'users_roles'
    extend_existing=True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))



