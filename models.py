from database import Base
from flask_security.models import sqla as sqla

class Role(Base, sqla.FsRoleMixin):
    __tablename__ = 'role'

class User(Base, sqla.FsUserMixin):
    __tablename__ = 'user'