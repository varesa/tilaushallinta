from sqlalchemy import (
    Column,

    Text,
    Integer,
    Float,
    DateTime,

    Index,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


"""class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)"""

class Tilaaja(Base):
    __tablename__ = 'tilaajat'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    date = Column(DateTime)

    nimi = Column(Text)
    yritys = Column(Text)

    osoite1 = Column(Text)
    osoite2 = Column(Text)

    puhelin = Column(Text)
    email = Column(Text)

class Kohde(Base):
    __tablename__ = 'kohteet'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    date = Column(DateTime)

    nimi = Column(Text)
    yritys = Column(Text)

    osoite1 = Column(Text)
    osoite2 = Column(Text)

    puhelin = Column(Text)
    email = Column(Text)

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
    id = Column(Integer)
    date = Column(DateTime)

    tilaaja_id = Column(Integer, ForeignKey("tilaajat.uuid"))
    tilaaja = relationship("Tilaaja", backref="tilaukset")

    kohde_id = Column(Integer, ForeignKey("kohteet.uuid"))
    kohde = relationship("Kohde", backref="tilaukset")

    muut_yhteysh = Column(Text)

    tyo = Column(Text)

    paivaraportit = relationship("Paivaraportti")
    tavarat = relationship("Tavara")

