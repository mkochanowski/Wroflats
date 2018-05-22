"""empty message

Revision ID: d84951de5b06
Revises: 
Create Date: 2018-05-21 12:53:56.202370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd84951de5b06'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coordinates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('full_name', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('coordinates_pairs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('origin_id', sa.Integer(), nullable=True),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.Column('time_transit', sa.Float(), nullable=True),
    sa.Column('time_on_foot', sa.Float(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('calculated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['origin_id'], ['coordinates.id'], ),
    sa.ForeignKeyConstraint(['target_id'], ['coordinates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=40), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=40), nullable=True),
    sa.Column('origin', sa.String(length=40), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=512), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('source_latitude', sa.Float(), nullable=True),
    sa.Column('source_longitude', sa.Float(), nullable=True),
    sa.Column('coordinates_id', sa.Integer(), nullable=True),
    sa.Column('is_scraped', sa.Boolean(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['coordinates_id'], ['coordinates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('areas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(length=40), nullable=True),
    sa.Column('center', sa.Integer(), nullable=True),
    sa.Column('radius', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['center'], ['coordinates.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submissions_calculated',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('parameters', sa.PickleType(), nullable=True),
    sa.Column('status', sa.String(length=40), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['submission_id'], ['submissions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_groups_assoc',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_id')
    )
    op.create_table('actions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(length=40), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['target_id'], ['submissions_calculated.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('submissions_calculated_pairs_assoc',
    sa.Column('pair_id', sa.Integer(), nullable=False),
    sa.Column('submission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pair_id'], ['coordinates_pairs.id'], ),
    sa.ForeignKeyConstraint(['submission_id'], ['submissions_calculated.id'], ),
    sa.PrimaryKeyConstraint('pair_id', 'submission_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('submissions_calculated_pairs_assoc')
    op.drop_table('actions')
    op.drop_table('users_groups_assoc')
    op.drop_table('submissions_calculated')
    op.drop_table('areas')
    op.drop_table('submissions')
    op.drop_table('sessions')
    op.drop_table('groups')
    op.drop_table('coordinates_pairs')
    op.drop_table('users')
    op.drop_table('coordinates')
    # ### end Alembic commands ###