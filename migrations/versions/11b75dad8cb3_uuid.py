"""uuid

Revision ID: 11b75dad8cb3
Revises: 9c83ab743905
Create Date: 2023-08-02 17:48:21.574193

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '11b75dad8cb3'
down_revision = '9c83ab743905'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detected_individuals', schema=None) as batch_op:
        batch_op.drop_constraint('detected_individuals_ibfk_3', type_='foreignkey')

    with op.batch_alter_table('detected_media', schema=None) as batch_op:
        batch_op.alter_column('detected_medium_id',
               existing_type=mysql.CHAR(length=32),
               type_=sa.String(length=32),
               existing_nullable=False)

    with op.batch_alter_table('empty_media', schema=None) as batch_op:
        batch_op.alter_column('empty_medium_id',
               existing_type=mysql.CHAR(length=32),
               type_=sa.String(length=32),
               existing_nullable=False)

    with op.batch_alter_table('individuals', schema=None) as batch_op:
        batch_op.drop_constraint('individuals_ibfk_4', type_='foreignkey')

    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('medium_id',
               existing_type=mysql.CHAR(length=32),
               type_=sa.String(length=32),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.alter_column('medium_id',
               existing_type=sa.String(length=32),
               type_=mysql.CHAR(length=32),
               existing_nullable=False)

    with op.batch_alter_table('individuals', schema=None) as batch_op:
        batch_op.create_foreign_key('individuals_ibfk_4', 'media', ['medium'], ['medium_id'])

    with op.batch_alter_table('empty_media', schema=None) as batch_op:
        batch_op.alter_column('empty_medium_id',
               existing_type=sa.String(length=32),
               type_=mysql.CHAR(length=32),
               existing_nullable=False)

    with op.batch_alter_table('detected_media', schema=None) as batch_op:
        batch_op.alter_column('detected_medium_id',
               existing_type=sa.String(length=32),
               type_=mysql.CHAR(length=32),
               existing_nullable=False)

    with op.batch_alter_table('detected_individuals', schema=None) as batch_op:
        batch_op.create_foreign_key('detected_individuals_ibfk_3', 'detected_media', ['medium'], ['detected_medium_id'])

    # ### end Alembic commands ###
