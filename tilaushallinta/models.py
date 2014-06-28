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

class Laitteet(Base):
    __tablename__ = 'laitteet'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    date = Column(DateTime)

    # Lämmönjakohuone

    ljh_vaihdin = Column(Text)
    ljh_vaihdin_vm = Column(Text)

    # Kaukolämpöventtiilit

    klv_patteriverkosto = Column(Text)
    klv_lattialammitys = Column(Text)
    klv_ilmastointi = Column(Text)
    klv_kayttovesi = Column(Text)

    # Varoventtiilit

    vv_patteriverkosto = Column(Text)
    vv_lattialammitys = Column(Text)
    vv_ilmastointi = Column(Text)
    vv_kayttovesi = Column(Text)

    # Paisunta-astiat

    pa_patteriverkosto = Column(Text)
    pa_lattialammitys = Column(Text)
    pa_ilmastointi = Column(Text)
    pa_kayttovesi = Column(Text)

    # Pumput

    p_patteriverkosto = Column(Text)
    p_lattialammitys = Column(Text)
    p_ilmastointi = Column(Text)
    p_kayttovesi = Column(Text)

    # Suodattimet

    s_patteriverkosto = Column(Text)
    s_lattialammitys = Column(Text)
    s_ilmastointi = Column(Text)
    s_kayttovesi = Column(Text)

    # Muuta huomioitavaa

    muu_huom = Column(Text)

class Vesikalusteiden_tklista(Base):
    __tablename__ = 'vk_tklistat'

    uuid = Column(Integer, primary_key=True)
    id = Column(Integer)
    date = Column(DateTime)

    kohde_id = Column(Integer, ForeignKey("kohteet.uuid"))

    este = Column(Text)
    sov_aika = Column(Text)

    ## tila = on/tarkistettu/ei
    ## tp = toimenpide: korjatttava/vaihdettava

    # Keittiö

    k_sekottaja_tila = Column(Text)
    k_sekottaja_tp = Column(Text)
    k_sekottaja_selitys = Column(Text)
    
    k_pkhana_tila = Column(Text)
    k_pkhana_tp = Column(Text)
    k_pkhana_selitys = Column(Text)
    
    k_hajulukko_tila = Column(Text)
    k_hajulukko_tp = Column(Text)
    k_hajulukko_selitys = Column(Text)
    
    k_viemliitos_tila = Column(Text) # Viemäriliitos
    k_viemliitos_tp = Column(Text)
    k_viemliitos_selitys = Column(Text)
    
    k_extra1_tila = Column(Text) # Extra/custom fields
    k_extra1_tp = Column(Text)
    k_extra1_selitys = Column(Text)
    
    k_extra2_tila = Column(Text)
    k_extra2_tp = Column(Text)
    k_extra2_selitys = Column(Text)
    
    k_extra3_tila = Column(Text)
    k_extra3_tp = Column(Text)
    k_extra3_selitys = Column(Text)
    
    # WC 1
    
    wc1_istuin_tila = Column(Text)
    wc1_istuin_tp = Column(Text)
    wc1_istuin_selitys = Column(Text)
    
    wc1_sulku_tila = Column(Text)
    wc1_sulku_tp = Column(Text)
    wc1_sulku_selitys = Column(Text)
    
    wc1_viemliitos_tila = Column(Text) # Viemäriliitos
    wc1_viemliitos_tp = Column(Text)
    wc1_viemliitos_selitys = Column(Text)
    
    wc1_wcsisa_tila = Column(Text) # Wc:n sisäosat
    wc1_wcsisa_tp = Column(Text)
    wc1_wcsisa_selitys = Column(Text)
    
    wc1_allassekottaja_tila = Column(Text)
    wc1_allassekottaja_tp = Column(Text)
    wc1_allassekottaja_selitys = Column(Text)
    
    wc1_suihkusekottaja_tila = Column(Text)
    wc1_suihkusekottaja_tp = Column(Text)
    wc1_suihkusekottaja_selitys = Column(Text)
    
    wc1_suihkuvarusteet_tila = Column(Text)
    wc1_suihkuvarusteet_tp = Column(Text)
    wc1_suihkuvarusteet_selitys = Column(Text)
    
    wc1_pkhana_tila = Column(Text)
    wc1_pkhana_tp = Column(Text)
    wc1_pkhana_selitys = Column(Text)
    
    wc1_vesilukko_tila = Column(Text)
    wc1_vesilukko_tp = Column(Text)
    wc1_vesilukko_selitys = Column(Text)
    
    wc1_lattiakaivo_tila = Column(Text)
    wc1_lattiakaivo_tp = Column(Text)
    wc1_lattiakaivo_selitys = Column(Text)
    
    wc1_kuivakaivo_tila = Column(Text)
    wc1_kuivakaivo_tp = Column(Text)
    wc1_kuivakaivo_selitys = Column(Text)
    
    wc1_kvpatteri_tila = Column(Text) # Käyttövesipatteri
    wc1_kvpatteri_tp = Column(Text)
    wc1_kvpatteri_selitys = Column(Text)
    
    wc1_extra1_tila = Column(Text)
    wc1_extra1_tp = Column(Text)
    wc1_extra1_selitys = Column(Text)
    
    wc1_extra2_tila = Column(Text)
    wc1_extra2_tp = Column(Text)
    wc1_extra2_selitys = Column(Text)
    
    wc1_extra3_tila = Column(Text)
    wc1_extra3_tp = Column(Text)
    wc1_extra3_selitys = Column(Text)
    
    wc1_wcmalli = Column(Text)
    
    # WC 2
    
    wc2_istuin_tila = Column(Text)
    wc2_istuin_tp = Column(Text)
    wc2_istuin_selitys = Column(Text)
    
    wc2_sulku_tila = Column(Text)
    wc2_sulku_tp = Column(Text)
    wc2_sulku_selitys = Column(Text)
    
    wc2_viemliitos_tila = Column(Text) # Viemäriliitos
    wc2_viemliitos_tp = Column(Text)
    wc2_viemliitos_selitys = Column(Text)
    
    wc2_wcsisa_tila = Column(Text) # Wc:n sisäosat
    wc2_wcsisa_tp = Column(Text)
    wc2_wcsisa_selitys = Column(Text)
    
    wc2_allassekottaja_tila = Column(Text)
    wc2_allassekottaja_tp = Column(Text)
    wc2_allassekottaja_selitys = Column(Text)
    
    wc2_extra1_tila = Column(Text)
    wc2_extra1_tp = Column(Text)
    wc2_extra1_selitys = Column(Text)
    
    wc2_extra2_tila = Column(Text)
    wc2_extra2_tp = Column(Text)
    wc2_extra2_selitys = Column(Text)
    
    wc2_extra3_tila = Column(Text)
    wc2_extra3_tp = Column(Text)
    wc2_extra3_selitys = Column(Text)
    
    wc2_wcmalli = Column(Text)

    huomiot = Column(Text)

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

    maksuaika = Column(Integer)

    paivaraportit = relationship("Paivaraportti")
    tavarat = relationship("Tavara")
    


