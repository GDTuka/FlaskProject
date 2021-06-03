"""new fields in user model

Revision ID: 9677d93ed659
Revises: 
Create Date: 2021-05-28 20:36:01.248169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9677d93ed659'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###