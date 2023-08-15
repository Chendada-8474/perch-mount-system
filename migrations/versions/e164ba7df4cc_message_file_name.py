"""message file name

Revision ID: e164ba7df4cc
Revises: 27a3c39e1ad3
Create Date: 2023-08-15 22:50:39.028571

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e164ba7df4cc'
down_revision = '27a3c39e1ad3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message_file_name', sa.String(length=30), nullable=True))
        batch_op.drop_column('file_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('file_name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=30), nullable=True))
        batch_op.drop_column('message_file_name')

    # ### end Alembic commands ###
