#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

import bcrypt

from sqlalchemy import Column, Text, Integer, DateTime, Boolean

from .meta import Base


class User(Base):
    __tablename__ = 'users'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    name = Column(Text)

    email = Column(Text)
    password_hash = Column(Text)

    admin = Column(Boolean)

    def hash_password(self, password, new=False):
        if new:
            salt = bcrypt.gensalt()
        else:
            salt = self.password_hash  # bcrypt stores salt in the beginning of the hash
        if not isinstance(salt, bytes):
            salt = salt.encode('utf-8')

        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def set_password(self, password):
        self.password_hash = self.hash_password(password, new=True)

    def verify_password(self, password):
        if isinstance(self.password_hash, bytes):
            password_hash = self.password_hash
        else:
            password_hash = self.password_hash.encode('utf-8')

        return password_hash == self.hash_password(password)
