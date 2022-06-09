"""empty message

Revision ID: 57357ea62ea5
Revises: 1de3e2c33fc4
Create Date: 2022-06-09 20:15:10.837068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57357ea62ea5'
down_revision = '1de3e2c33fc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.create_foreign_key(None, 'log', 'log_categories', ['category_id'], ['id'])
    op.drop_column('log', 'category')
    op.add_column('users', sa.Column('status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'status')
    op.add_column('log', sa.Column('category', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.create_foreign_key(None, 'log', 'log_categories', ['category'], ['id'])
    # ### end Alembic commands ###
