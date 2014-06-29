#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Author: Esa Varemo
#

from sqlalchemy import Column, Text, Integer, DateTime, Boolean

from .meta import Base


class User(Base):
    __tablename__ = 'users'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    dateCreated = Column(DateTime)

    username = Column(Text)
    password = Column(Text)
    password_salt = Column(Text)

    isAdmin = Column(Boolean)