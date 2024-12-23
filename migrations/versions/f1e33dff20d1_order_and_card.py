"""order and card

Revision ID: f1e33dff20d1
Revises: f62b7f583e3f
Create Date: 2024-12-17 19:27:02.052940

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f1e33dff20d1'
down_revision = 'f62b7f583e3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_number', sa.String(length=15), nullable=False))
        batch_op.add_column(sa.Column('shipping_address', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('total_price', sa.Float(), nullable=False))
        batch_op.alter_column('customer_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
        batch_op.drop_column('total_amount')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_amount', mysql.FLOAT(), nullable=False))
        batch_op.alter_column('customer_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_column('total_price')
        batch_op.drop_column('shipping_address')
        batch_op.drop_column('contact_number')

    # ### end Alembic commands ###
