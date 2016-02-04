#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, Date
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

    tyyppi_ke = Column(Boolean)
    ke_starting_date = Column(Date)

    tyyppi_sy = Column(Boolean)
    sy_starting_date = Column(Date)

    tyyppi_tk = Column(Boolean)
    tk_interval_months = Column(Float)
    tk_starting_date = Column(Date)
