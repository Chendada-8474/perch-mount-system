"""empty message

Revision ID: b6ed60e93041
Revises: 0bfa275c6555
Create Date: 2023-08-07 11:54:02.790408

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b6ed60e93041'
down_revision = '0bfa275c6555'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('behaviors',
    sa.Column('behavior_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chinese_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('behavior_id')
    )
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.add_column(sa.Column('featured_discription', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('featured_behavior', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'behaviors', ['featured_behavior'], ['behavior_id'])

    with op.batch_alter_table('perch_mounts', schema=None) as batch_op:
        batch_op.alter_column('habitat',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('project',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('perch_mounts', schema=None) as batch_op:
        batch_op.alter_column('project',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('habitat',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('featured_behavior')
        batch_op.drop_column('featured_discription')

    op.drop_table('behaviors')
    # ### end Alembic commands ###