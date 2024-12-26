"""Adjusting category and relationshp

Revision ID: 8b2e7e31caa7
Revises: 20f1acb59214
Create Date: 2024-12-12 13:34:07.765161

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8b2e7e31caa7'
down_revision = '20f1acb59214'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.String(length=100), nullable=False),
    sa.Column('category_image_path', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('category_id'),
    sa.UniqueConstraint('category_name')
    )
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_index('product_name')

    op.drop_table('category')
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'categories', ['product_category_id'], ['category_id'])
        batch_op.drop_column('product_category')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_category', mysql.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('product_category_id')

    op.create_table('category',
    sa.Column('product_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('product_image_path', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('category_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.create_index('product_name', ['product_name'], unique=True)

    op.drop_table('categories')
    # ### end Alembic commands ###