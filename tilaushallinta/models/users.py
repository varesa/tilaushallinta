#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#
import bcrypt

from sqlalchemy import Column, Text, Integer, DateTime, Boolean

from .meta import Base


class User(Base):
    __tablename__ = 'users'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    dateCreated = Column(DateTime)

    username = Column(Text)
    password = Column(Text)

    email = Column(Text)

    isAdmin = Column(Boolean)

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = self.password # Get salt from beginning of the password
        return bcrypt.hashpw(password, salt)

    def set_password(self, password):
        self.password = self.encrypt_password(password, salt=bcrypt.gensalt())

    def verify_password(self, password):
        return self.password == self.encrypt_password(password)
