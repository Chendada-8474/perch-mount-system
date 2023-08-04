"""uuid as medium id

Revision ID: 717e64b9eba4
Revises: 324f112dd3d0
Create Date: 2023-08-02 16:26:50.346706

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '717e64b9eba4'
down_revision = '324f112dd3d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detected_individuals', schema=None) as batch_op:
        batch_op.alter_column('pending_individual_id',
               existing_type=mysql.VARCHAR(length=22),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('medium',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=22),
               existing_nullable=True)

    with op.batch_alter_table('detected_media', schema=None) as batch_op:
        batch_op.alter_column('detected_medium_id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=22),
               existing_nullable=False)

    with op.batch_alter_table('empty_media', schema=None) as batch_op:
        batch_op.alter_column('empty_medium_id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=22),
               existing_nullable=False)

    with op.batch_alter_table('individuals', schema=None) as batch_op:
        batch_op.alter_column('medium',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=22),
               existing_nullable=True)

    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('medium_id',
               existing_type=mysql.INTEGER(),
               type_=sa.String(length=22),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('medium_id',
               existing_type=sa.String(length=22),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('individuals', schema=None) as batch_op:
        batch_op.alter_column('medium',
               existing_type=sa.String(length=22),
               type_=mysql.INTEGER(),
               existing_nullable=True)

    with op.batch_alter_table('empty_media', schema=None) as batch_op:
        batch_op.alter_column('empty_medium_id',
               existing_type=sa.String(length=22),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('detected_media', schema=None) as batch_op:
        batch_op.alter_column('detected_medium_id',
               existing_type=sa.String(length=22),
               type_=mysql.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('detected_individuals', schema=None) as batch_op:
        batch_op.alter_column('medium',
               existing_type=sa.String(length=22),
               type_=mysql.INTEGER(),
               existing_nullable=True)
        batch_op.alter_column('pending_individual_id',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=22),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###
