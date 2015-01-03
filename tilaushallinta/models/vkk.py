#
# This source code is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/4.0/.
# Copyright Esa Varemo 2014-2015
#

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .meta import Base


class Vesikalustekartoitus(Base):
    __versioned__ = {}
    __tablename__ = 'vesikalustekartoitukset'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    # Property relationships
    kohde_id = Column(Integer, ForeignKey('kohteet.id'))
    kohde = relationship("Kohde", backref="vesikalustekartoitukset")

    # Relationships down
    asunnot = relationship("VKK_Asunto")


# noinspection PyPep8Naming
class VKK_Asunto(Base):
    __versioned__ = {}
    __tablename__ = 'vkk_asunnot'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    # Up relationships support
    vkk_id = Column(Integer, ForeignKey('vesikalustekartoitukset.id'))

    # Properties
    numero = Column(Text)

    # Relationships down
    huoneet = relationship("VKK_Huone")


# noinspection PyPep8Naming
class VKK_Huone(Base):
    __versioned__ = {}
    __tablename__ = 'vkk_huoneet'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    # Up relationships support
    asunto_id = Column(Integer, ForeignKey('vkk_asunnot.id'))

    # Properties
    nimi = Column(Text, nullable=False)

    # Relationships down
    kalusteet = relationship("VKK_Kaluste")


# noinspection PyPep8Naming
class VKK_Kaluste(Base):
    __versioned__ = {}
    __tablename__ = 'vkk_kalusteet'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)

    # Up relationships support
    huone_id = Column(Integer, ForeignKey('vkk_huoneet.id'))

    # Properties
    nimi = Column(Text, nullable=False)
    koodi = Column(Text)
    maara = Column(Integer, nullable=False)
    tila = Column(Enum("Korjaus", "Vaihto", "Ok", name="enum_kaluste_tila"), nullable=False)
