#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from sqlalchemy import Column, Float, Integer

from .meta import Base


class Hintaluokka(Base):
    __tablename__ = 'hintaluokat'

    hintaluokka = Column(Integer, primary_key=True)

    tunnit = Column(Float)
    matkat = Column(Float)