"""empty message

Revision ID: 452a6faae00
Revises: 2630fa50c62
Create Date: 2015-09-14 20:06:06.504389

"""

# revision identifiers, used by Alembic.
revision = '452a6faae00'
down_revision = '2630fa50c62'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql

Session = sessionmaker(bind=op.get_bind())()

meta = sa.MetaData()
meta.reflect(bind=op.get_bind())

Base = declarative_base()


class Tilaajat_tmp(Base):
    __tablename__ = "tilaajat_tmp"
    id = sa.Column(sa.Integer, primary_key=True)
    slaskutus = sa.Column(sa.Text)



t_tilaajat = sa.Table('tilaajat', meta)
"""t_tilaajat_tmp = sa.Table('tilaajat_tmp', meta,
                          sa.Column('id', sa.Integer, primary_key=True),
                          sa.Column('slaskutus', sa.Text))

"""
t_kohteet = sa.Table('kohteet', meta)
"""t_kohteet_tmp = sa.Table('kohteet_tmp', meta,
                         sa.Column('id', sa.Integer, primary_key=True),
                         sa.Column('slaskutus', sa.Text))
"""

t_tilaukset = sa.Table('tilaukset', meta)

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###

    op.add_column('kohteet', sa.Column('slaskutus', sa.Text(), nullable=True))
    op.add_column('kohteet_version', sa.Column('slaskutus', sa.Text(), autoincrement=False, nullable=True))

    for tilaus in Session.query(t_tilaukset).all():
        tilaaja_id = tilaus.tilaaja_id
        tilaaja = Session.query(t_tilaajat).filter_by(id=tilaaja_id).first()
        kohde_id = tilaus.kohde_id
        kohde = Session.query(t_kohteet).filter_by(id=kohde_id).first()
        kohde.slaskutus = tilaaja.slaskutus

    Session.commit()
    Session.close()

    op.drop_column('tilaajat', 'slaskutus')
    op.drop_column('tilaajat_version', 'slaskutus')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tilaajat_version', sa.Column('slaskutus', mysql.TEXT(), nullable=True))
    op.add_column('tilaajat', sa.Column('slaskutus', mysql.TEXT(), nullable=True))

    for tilaus in Session.query(t_tilaukset).all():
        tilaaja_id = tilaus.tilaaja_id
        tilaaja = Session.query(t_tilaajat).filter_by(id=tilaaja_id).first()
        kohde_id = tilaus.kohde_id
        kohde = Session.query(t_kohteet).filter_by(id=kohde_id).first()
        tilaaja.slaskutus = kohde.slaskutus

    Session.commit()
    Session.close()

    op.drop_column('kohteet_version', 'slaskutus')
    op.drop_column('kohteet', 'slaskutus')
    ### end Alembic commands ###