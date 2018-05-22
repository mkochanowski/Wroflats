"""empty message

Revision ID: 400267fb0d09
Revises: d84951de5b06
Create Date: 2018-05-21 13:40:45.333830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '400267fb0d09'
down_revision = 'd84951de5b06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('submissions', sa.Column('images', sa.PickleType(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('submissions', 'images')
    # ### end Alembic commands ###