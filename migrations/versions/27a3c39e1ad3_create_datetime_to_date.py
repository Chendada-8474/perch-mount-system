"""create datetime to date

Revision ID: 27a3c39e1ad3
Revises: c03a8aa7bded
Create Date: 2023-08-15 22:50:05.084924

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '27a3c39e1ad3'
down_revision = 'c03a8aa7bded'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('checked', sa.Boolean(), nullable=True))
        batch_op.drop_column('opened')
        batch_op.drop_column('create_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('update_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_time', mysql.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('opened', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.drop_column('checked')
        batch_op.drop_column('create_date')

    # ### end Alembic commands ###