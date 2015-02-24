#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from .meta import Base


class Paivaraportti(Base):
    __versioned__ = {}
    __tablename__ = 'paivarapotit'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    tilaus_id = Column(Integer, ForeignKey("tilaukset.id"), default=2)

    teksti = Column(Text)

    hintaluokka = Column(Integer, nullable=False)

    tunnit = Column(Float)
    matkat = Column(Float)
    muut = Column(Float)


class Tavara(Base):
    __versioned__ = {}
    __tablename__ = 'tavarat'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    tilaus_id = Column(Integer, ForeignKey("tilaukset.id"))

    koodi = Column(Text)
    nimi = Column(Text)

    hinta = Column(Float)
    maara = Column(Float)
    yksikko = Column(Text)

    tyyppi = Column(Text)


class Tilaus(Base):
    __versioned__ = {}
    __tablename__ = 'tilaukset'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    TILA_UUSI = "UUSI"
    TILA_HYVAKSYTTY = "HYVAKSYTTY"
    TILA_ALOITETTU = "ALOITETTU"
    TILA_VALMIS = "VALMIS"
    tila = Column(String(15), nullable=False, default=TILA_UUSI)

    viitenumero = Column(Text)

    tilaaja_id = Column(Integer, ForeignKey("tilaajat.id"))
    tilaaja = relationship("Tilaaja", backref="tilaukset")

    kohde_id = Column(Integer, ForeignKey("kohteet.id"))
    kohde = relationship("Kohde", backref="tilaukset")

    muut_yhteysh = Column(Text)

    tyo = Column(Text)

    maksuaika = Column(Integer)

    paivaraportit = relationship("Paivaraportti")
    tavarat = relationship("Tavara")