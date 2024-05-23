"""empty message

Revision ID: 03fa6d6a6fab
Revises: 
Create Date: 2024-05-14 12:50:04.183111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03fa6d6a6fab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('People', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('People', sa.Column('gender', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('People', 'gender')
    op.drop_column('People', 'age')
    # ### end Alembic commands ###
