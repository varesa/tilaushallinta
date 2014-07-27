"""empty message

Revision ID: 59fbf3b1730
Revises: 42129b3413e
Create Date: 2014-07-14 10:54:06.106969

"""

# revision identifiers, used by Alembic.
revision = '59fbf3b1730'
down_revision = '42129b3413e'

import sqlalchemy as sa

from tilaushallinta.alembic import op


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.Text(), nullable=True))
    op.drop_column('users', 'username')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.TEXT(), nullable=True))
    op.drop_column('users', 'name')
    ### end Alembic commands ###
