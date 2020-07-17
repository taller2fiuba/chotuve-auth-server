"""empty message

Revision ID: 6513babed1bc
Revises: 20a8d438e23b
Create Date: 2020-07-16 14:35:07.038767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6513babed1bc'
down_revision = '20a8d438e23b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_server',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_app_server_url'), 'app_server', ['url'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_app_server_url'), table_name='app_server')
    op.drop_table('app_server')
    # ### end Alembic commands ###