#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014
#

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .meta import Base


class Vesikalustekartoitus(Base):
    __tablename__ = 'vesikalustekartoitukset'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    # Property relationships
    kohde_id = Column(Integer, ForeignKey('kohteet.id'))
    kohde = relationship("Kohde", backref="vesikalustekartoitukset")

    # Relationships down
    asunnot = relationship("VKK_Asunto")


# noinspection PyPep8Naming
class VKK_Asunto(Base):
    __tablename__ = 'vkk_asunnot'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    # Up relationships support
    vkk_uuid = Column(Integer, ForeignKey('vesikalustekartoitukset.uuid'))

    # Properties
    numero = Column(Text)

    # Relationships down
    huoneet = relationship("VKK_Huone")


# noinspection PyPep8Naming
class VKK_Huone(Base):
    __tablename__ = 'vkk_huoneet'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    # Up relationships support
    asunto_uuid = Column(Integer, ForeignKey('vkk_asunnot.uuid'))

    # Properties
    nimi = Column(Text, nullable=False)

    # Relationships down
    kalusteet = relationship("VKK_Kaluste")


# noinspection PyPep8Naming
class VKK_Kaluste(Base):
    __tablename__ = 'vkk_kalusteet'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    # Up relationships support
    huone_uuid = Column(Integer, ForeignKey('vkk_huoneet.uuid'))

    # Properties
    nimi = Column(Text, nullable=False)
    koodi = Column(Text)
    maara = Column(Integer, nullable=False)
    tila = Column(Enum("Korjaus", "Vaihto", "Ok", name="enum_kaluste_tila"), nullable=False)