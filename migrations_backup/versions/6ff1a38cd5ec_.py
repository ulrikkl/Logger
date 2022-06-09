"""empty message

Revision ID: 6ff1a38cd5ec
Revises: fea9ac831ee7
Create Date: 2022-06-02 14:10:08.374707

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ff1a38cd5ec'
down_revision = 'fea9ac831ee7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.create_foreign_key(None, 'log', 'log_categories', ['category_id'], ['id'])
    op.drop_column('log', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('log', sa.Column('category', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.create_foreign_key(None, 'log', 'log_categories', ['category'], ['id'])
    # ### end Alembic commands ###