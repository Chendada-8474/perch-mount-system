"""perch mount column of detection

Revision ID: 37d34745cf11
Revises: fdb7021a0337
Create Date: 2023-08-22 23:51:33.178903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37d34745cf11'
down_revision = 'fdb7021a0337'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedule_detect', schema=None) as batch_op:
        batch_op.add_column(sa.Column('perch_mount', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'perch_mounts', ['perch_mount'], ['perch_mount_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedule_detect', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('perch_mount')

    # ### end Alembic commands ###
