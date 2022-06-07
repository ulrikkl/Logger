"""empty message

Revision ID: 7c13c5b5475d
Revises: 8728b87d810f
Create Date: 2022-06-02 14:03:10.856533

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c13c5b5475d'
down_revision = '8728b87d810f'
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