#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from sqlalchemy import Column, Integer, DateTime, Text

from .meta import Base


class Tilaaja(Base):
    __tablename__ = 'tilaajat'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    nimi = Column(Text)
    yritys = Column(Text)
    ytunnus = Column(Text)

    osoite = Column(Text)
    postinumero = Column(Text)
    postitoimipaikka = Column(Text)

    puhelin = Column(Text)
    email = Column(Text)

    slaskutus = Column(Text)