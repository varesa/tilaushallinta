#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .meta import Base


class Kohde(Base):
    __tablename__ = 'kohteet'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    laitteet_id = Column(Integer, ForeignKey("laitteet.uuid"))
    laitteet = relationship("Laitteet", backref="kohde")

    vk_tklistat = relationship("Vesikalusteiden_tklista")

    nimi = Column(Text)
    yritys = Column(Text)
    ytunnus = Column(Text)

    osoite = Column(Text)
    postinumero = Column(Text)
    postitoimipaikka = Column(Text)

    puhelin = Column(Text)
    email = Column(Text)