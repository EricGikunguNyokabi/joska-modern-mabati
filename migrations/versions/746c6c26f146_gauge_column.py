"""gauge column

Revision ID: 746c6c26f146
Revises: 058a686a8a05
Create Date: 2024-12-26 23:19:29.322944

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '746c6c26f146'
down_revision = '058a686a8a05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_gauge', sa.Integer(), nullable=True))
        batch_op.drop_column('product_gauges')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_gauges', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.drop_column('product_gauge')

    # ### end Alembic commands ###
