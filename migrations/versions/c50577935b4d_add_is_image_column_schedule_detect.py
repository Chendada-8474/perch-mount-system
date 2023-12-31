"""add is_image column schedule detect

Revision ID: c50577935b4d
Revises: b5b5da8ce964
Create Date: 2023-08-23 12:00:07.436409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c50577935b4d'
down_revision = 'b5b5da8ce964'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedule_detect', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_image', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('schedule_detect', schema=None) as batch_op:
        batch_op.drop_column('is_image')

    # ### end Alembic commands ###
