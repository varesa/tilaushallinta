from sqlalchemy import Column, Integer, DateTime, Text

from .meta import Base


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