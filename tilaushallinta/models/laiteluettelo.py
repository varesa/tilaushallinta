#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from .meta import Base


class Laite(Base):
    __versioned__ = {}
    __tablename__ = 'laitteet'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    tavaraluettelo_id = Column(Integer, ForeignKey("laiteluettelot.id"))

    nimi = Column(Text)
    tyyppitiedot = Column(Text)

    valmistusvuosi = Column(Float)
    maara = Column(Float)

    tyyppi = Column(Text)


class Laiteluettelo(Base):
    __versioned__ = {}
    __tablename__ = 'laiteluettelot'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    laitteet = relationship("Laite", backref="laiteluettelo")

    huoltosopimus_id = Column(Integer, ForeignKey("huoltosopimukset.id"))
    huoltosopimus = relationship("Huoltosopimus", backref="tavaraluettelot")
