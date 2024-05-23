"""empty message

Revision ID: d8a7d2a545d9
Revises: 03fa6d6a6fab
Create Date: 2024-05-14 15:45:31.637283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8a7d2a545d9'
down_revision = '03fa6d6a6fab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Movies_person_id_fkey', 'Movies', type_='foreignkey')
    op.drop_column('Movies', 'person_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Movies', sa.Column('person_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('Movies_person_id_fkey', 'Movies', 'People', ['person_id'], ['id'])
    # ### end Alembic commands ###
