"""adjusting categiry_id

Revision ID: 20f1acb59214
Revises: bf8510be8adf
Create Date: 2024-12-12 13:20:11.758604

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '20f1acb59214'
down_revision = 'bf8510be8adf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.drop_column('product_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False))
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###