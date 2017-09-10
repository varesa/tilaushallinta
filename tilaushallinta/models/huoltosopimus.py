#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2016
#

from dateutil.relativedelta import relativedelta

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, Date
from sqlalchemy.orm import relationship

from .meta import Base
from .huolto import Huolto

DAYS_PER_WEEK = 7
DAYS_PER_MONTH = 365 / 12


class Huoltosopimus(Base):
    __versioned__ = {}
    __tablename__ = 'huoltosopimukset'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    # Contract states
    TILA_ACTIVE = "ACTIVE"
    TILA_INACTIVE = "INACTIVE"

    # State
    tila = Column(String(15), nullable=False, default=TILA_ACTIVE)

    # Optional reference number
    viitenumero = Column(Text)

    # Customer
    tilaaja_id = Column(Integer, ForeignKey("tilaajat.id"))
    tilaaja = relationship("Tilaaja", backref="huoltosopimukset")

    # Work location
    kohde_id = Column(Integer, ForeignKey("kohteet.id"))
    kohde = relationship("Kohde", backref="huoltosopimukset")

    # Other contact details
    muut_yhteysh = Column(Text)

    # Maintenance type: Keväthuolto
    tyyppi_ke = Column(Boolean)
    ke_starting_date = Column(Date)
    ke_next_date = Column(Date)
    ke_interval_months = 12

    # Maintenance type: Syyshuolto
    tyyppi_sy = Column(Boolean)
    sy_starting_date = Column(Date)
    sy_next_date = Column(Date)
    sy_interval_months = 12

    # Maintenance type: Tarkastuskäynti
    tyyppi_tk = Column(Boolean)
    tk_starting_date = Column(Date)
    tk_next_date = Column(Date)
    tk_interval_months = Column(Float)

    def advance_date(self, maintenance_type):
        if maintenance_type == Huolto.TYYPPI_KE:
            print(self.ke_next_date)
            self.ke_next_date += relativedelta(months=self.ke_interval_months)
        elif maintenance_type == Huolto.TYYPPI_SY:
            self.sy_next_date += relativedelta(months=self.sy_interval_months)
        elif maintenance_type == Huolto.TYYPPI_TK:
            if self.tk_interval_months >= 1:
                self.tk_next_date += \
                    relativedelta(months=int(self.tk_interval_months))
            else:
                self.tk_next_date += \
                    relativedelta(weeks=int(self.tk_interval_months * DAYS_PER_MONTH / DAYS_PER_WEEK))

