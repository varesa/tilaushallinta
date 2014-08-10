#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .meta import Base


class Paivaraportti(Base):
    __tablename__ = 'paivarapotit'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    date = Column(DateTime)

    tilaus_id = Column(Integer, ForeignKey("tilaukset.uuid"))

    teksti = Column(Text)

    tunnit = Column(Float)
    matkat = Column(Float)
    muut = Column(Float)


class Tavara(Base):
    __tablename__ = 'tavarat'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    date = Column(DateTime)

    tilaus_id = Column(Integer, ForeignKey("tilaukset.uuid"))

    koodi = Column(Text)
    nimi = Column(Text)

    tyyppi = Column(Text)
    maara = Column(Integer)


class Tilaus(Base):
    __tablename__ = 'tilaukset'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    viitenumero = Column(Text)

    tilaaja_id = Column(Integer, ForeignKey("tilaajat.uuid"))
    tilaaja = relationship("Tilaaja", backref="tilaukset")

    kohde_id = Column(Integer, ForeignKey("kohteet.uuid"))
    kohde = relationship("Kohde", backref="tilaukset")

    muut_yhteysh = Column(Text)

    tyo = Column(Text)

    maksuaika = Column(Integer)

    paivaraportit = relationship("Paivaraportti")
    tavarat = relationship("Tavara")