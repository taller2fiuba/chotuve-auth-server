"""empty message

Revision ID: 20a8d438e23b
Revises: 0e3a3a3b480c
Create Date: 2020-06-18 06:57:27.284492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20a8d438e23b'
down_revision = '0e3a3a3b480c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('habilitado', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'habilitado')
    # ### end Alembic commands ###