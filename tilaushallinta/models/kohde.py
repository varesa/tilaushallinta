from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .meta import Base


class Kohde(Base):
    __tablename__ = 'kohteet'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    date = Column(DateTime)

    laitteet_id = Column(Integer, ForeignKey("laitteet.uuid"))
    laitteet = relationship("Laitteet", backref="kohde")

    vk_tklistat = relationship("Vesikalusteiden_tklista")

    nimi = Column(Text)
    yritys = Column(Text)

    osoite1 = Column(Text)
    osoite2 = Column(Text)

    puhelin = Column(Text)
    email = Column(Text)