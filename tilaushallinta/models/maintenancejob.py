#
# This source code is licensed under the terms of the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from .meta import Base


class MaintenanceReport(Base):
    __versioned__ = {}
    __tablename__ = 'huoltorapotit'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    huolto_id = Column(Integer, ForeignKey("huollot.id"))

    teksti = Column(Text)

    korjaustarve = Column(Boolean)


class MaintenanceOperation(Base):
    __versioned__ = {}
    __tablename__ = 'lisatoimenpiteet'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    huolto_id = Column(Integer, ForeignKey("huollot.id"))

    teksti = Column(Text)

    hintaluokka = Column(Integer, nullable=False)

    tunnit = Column(Float)
    matkat = Column(Float)
    muut = Column(Float)


class MaintenanceJob(Base):
    __versioned__ = {}
    __tablename__ = 'huollot'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    TILA_UUSI = "UUSI"
    TILA_ALOITETTU = "ALOITETTU"
    TILA_VALMIS = "VALMIS"
    tila = Column(String(15), nullable=False, default=TILA_UUSI)

    huoltosopimus_id = Column(Integer, ForeignKey("huoltosopimukset.id"))
    huoltosopimus = relationship("Huoltosopimus", backref="huollot")

    tyyppi = Column(Text)
    TYYPPI_EK = "ek"
    TYYPPI_KE = "ke"
    TYYPPI_SY = "sy"
    TYYPPI_TK = "tk"

    hintaluokka_id = Column(Integer, ForeignKey("huoltohintaluokat.hintaluokka"))
    hintaluokka = relationship("HuoltoHintaluokka", backref="huollot")

    huoltoraportit = relationship("MaintenanceReport")
    lisatoimenpiteet = relationship("MaintenanceOperation")

    laiteluettelo_id = Column(Integer, ForeignKey("laiteluettelot.id"))
    laiteluettelo = relationship("Laiteluettelo")

