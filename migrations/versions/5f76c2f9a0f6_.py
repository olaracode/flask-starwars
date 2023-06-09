"""empty message

Revision ID: 5f76c2f9a0f6
Revises: 3057de6206b4
Create Date: 2023-04-20 22:28:39.849745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f76c2f9a0f6'
down_revision = '3057de6206b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('eye_color', sa.String(length=17), nullable=True),
    sa.Column('homeworld', sa.String(length=80), nullable=True),
    sa.Column('gender', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('character')
    # ### end Alembic commands ###
