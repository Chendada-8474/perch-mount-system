"""ring number type

Revision ID: a57e0e404177
Revises: bb56ee83d851
Create Date: 2023-08-02 20:54:55.546710

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a57e0e404177'
down_revision = 'bb56ee83d851'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('individuals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ring_number', sa.String(length=15), nullable=True))
        batch_op.drop_column('rung_number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('individuals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rung_number', mysql.VARCHAR(length=15), nullable=True))
        batch_op.drop_column('ring_number')

    # ### end Alembic commands ###
