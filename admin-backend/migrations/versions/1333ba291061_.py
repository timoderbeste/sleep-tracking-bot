"""empty message

Revision ID: 1333ba291061
Revises: None
Create Date: 2019-07-02 21:24:08.641810

"""

# revision identifiers, used by Alembic.
revision = '1333ba291061'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userName', sa.String(length=64), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('currentPlan', sa.String(length=64), nullable=True),
    sa.Column('personalInfo', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_phone'), 'users', ['phone'], unique=True)
    op.create_table('data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('isUser', sa.Boolean(), nullable=False),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('isSlept', sa.Boolean(), nullable=False),
    sa.Column('reason', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('records')
    op.drop_table('data')
    op.drop_index(op.f('ix_users_phone'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
