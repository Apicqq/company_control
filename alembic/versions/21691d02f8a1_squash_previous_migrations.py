"""Squash previous migrations

Revision ID: 21691d02f8a1
Revises: 
Create Date: 2024-12-17 13:33:46.428823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import LtreeType


# revision identifiers, used by Alembic.
revision: str = '21691d02f8a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS ltree')
    op.create_table('company',
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_company')),
    sa.UniqueConstraint('company_name', name=op.f('uq_company_company_name'))
    )
    op.create_table('invitechallenge',
    sa.Column('account', sa.String(), nullable=False),
    sa.Column('invite_token', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_invitechallenge')),
    sa.UniqueConstraint('account', 'invite_token', name='invite_token_unique')
    )
    op.create_table('user',
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('account', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('USER', 'ADMIN', name='role'), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name=op.f('fk_user_company_id_company')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('account', name=op.f('uq_user_account'))
    )
    op.create_table('department',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('path', LtreeType(), nullable=False),
    sa.Column('parent_department', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('head_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], name=op.f('fk_department_company_id_company')),
    sa.ForeignKeyConstraint(['head_id'], ['user.id'], name=op.f('fk_department_head_id_user')),
    sa.ForeignKeyConstraint(['parent_department'], ['department.id'], name=op.f('fk_department_parent_department_department')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_department')),
    sa.UniqueConstraint('company_id', 'name', name='unique_department_name'),
    sa.UniqueConstraint('company_id', 'path', name='unique_path')
    )
    op.create_table('position',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], name=op.f('fk_position_department_id_department')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_position')),
    sa.UniqueConstraint('department_id', 'title', name='unique_position_title')
    )
    op.create_table('userposition',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('position_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['position_id'], ['position.id'], name=op.f('fk_userposition_position_id_position')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_userposition_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_userposition'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userposition')
    op.drop_table('position')
    op.drop_table('department')
    op.drop_table('user')
    op.drop_table('invitechallenge')
    op.drop_table('company')
    # ### end Alembic commands ###
