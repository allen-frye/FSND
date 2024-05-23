"""empty message

Revision ID: f1f805cda95a
Revises: aafaa2e149c8
Create Date: 2024-05-15 13:39:02.469125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1f805cda95a'
down_revision = 'aafaa2e149c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Movies_person_id_fkey', 'Movies', type_='foreignkey')
    op.drop_column('Movies', 'person_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Movies', sa.Column('person_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Movies_person_id_fkey', 'Movies', 'People', ['person_id'], ['id'])
    # ### end Alembic commands ###
