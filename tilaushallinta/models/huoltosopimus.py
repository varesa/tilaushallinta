#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .meta import Base


class Huoltosopimus(Base):
    __versioned__ = {}
    __tablename__ = 'huoltosopimukset'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    TILA_ACTIVE = "ACTIVE"
    TILA_INACTIVE = "INACTIVE"
    tila = Column(String(15), nullable=False, default=TILA_ACTIVE)

    viitenumero = Column(Text)

    tilaaja_id = Column(Integer, ForeignKey("tilaajat.id"))
    tilaaja = relationship("Tilaaja", backref="huoltosopimukset")

    kohde_id = Column(Integer, ForeignKey("kohteet.id"))
    kohde = relationship("Kohde", backref="huoltosopimukset")

    muut_yhteysh = Column(Text)

    tyyppi_ek = Column(Boolean)
    tyyppi_ke = Column(Boolean)
    tyyppi_sy = Column(Boolean)
    tyyppi_tk = Column(Boolean)
