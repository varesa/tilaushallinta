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

    name = Column(Text)

    email = Column(Text)
    password_hash = Column(Text)


    isAdmin = Column(Boolean)

    def hash_password(self, password, new=False):
        if new:
            salt = bcrypt.gensalt()
        else:
            salt = self.password_hash
        return bcrypt.hashpw(password, salt)

    def set_password(self, password):
        self.password_hash = self.encrypt_password(password, new=True)

    def verify_password(self, password):
        return self.password == self.hash_password(password)
