"""empty message

Revision ID: 310d4500779
Revises: 4a81e505ae1
Create Date: 2015-08-04 22:58:16.240782

"""

# revision identifiers, used by Alembic.
revision = '310d4500779'
down_revision = '4a81e505ae1'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('huoltosopimukset_version',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('date', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('tila', sa.String(length=15), autoincrement=False, nullable=True),
    sa.Column('viitenumero', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('tilaaja_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('kohde_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('muut_yhteysh', sa.Text(), autoincrement=False, nullable=True),
    sa.Column('tyyppi_ek', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('tyyppi_ke', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('tyyppi_sy', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('tyyppi_tk', sa.Boolean(), autoincrement=False, nullable=True),
    sa.Column('transaction_id', sa.BigInteger(), autoincrement=False, nullable=False),
    sa.Column('end_transaction_id', sa.BigInteger(), nullable=True),
    sa.Column('operation_type', sa.SmallInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id', 'transaction_id')
    )
    op.create_index(op.f('ix_huoltosopimukset_version_end_transaction_id'), 'huoltosopimukset_version', ['end_transaction_id'], unique=False)
    op.create_index(op.f('ix_huoltosopimukset_version_operation_type'), 'huoltosopimukset_version', ['operation_type'], unique=False)
    op.create_index(op.f('ix_huoltosopimukset_version_transaction_id'), 'huoltosopimukset_version', ['transaction_id'], unique=False)
    op.create_table('huoltosopimukset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('tila', sa.String(length=15), nullable=False),
    sa.Column('viitenumero', sa.Text(), nullable=True),
    sa.Column('tilaaja_id', sa.Integer(), nullable=True),
    sa.Column('kohde_id', sa.Integer(), nullable=True),
    sa.Column('muut_yhteysh', sa.Text(), nullable=True),
    sa.Column('tyyppi_ek', sa.Boolean(), nullable=True),
    sa.Column('tyyppi_ke', sa.Boolean(), nullable=True),
    sa.Column('tyyppi_sy', sa.Boolean(), nullable=True),
    sa.Column('tyyppi_tk', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['kohde_id'], ['kohteet.id'], ),
    sa.ForeignKeyConstraint(['tilaaja_id'], ['tilaajat.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('users', 'admin',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('users', 'vuosihuoltosopimukset',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'vuosihuoltosopimukset',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.alter_column('users', 'admin',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.drop_table('huoltosopimukset')
    op.drop_index(op.f('ix_huoltosopimukset_version_transaction_id'), table_name='huoltosopimukset_version')
    op.drop_index(op.f('ix_huoltosopimukset_version_operation_type'), table_name='huoltosopimukset_version')
    op.drop_index(op.f('ix_huoltosopimukset_version_end_transaction_id'), table_name='huoltosopimukset_version')
    op.drop_table('huoltosopimukset_version')
    ### end Alembic commands ###