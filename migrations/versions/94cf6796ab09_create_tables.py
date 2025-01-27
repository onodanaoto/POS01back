"""create tables

Revision ID: 94cf6796ab09
Revises: 
Create Date: 2024-01-26 14:47:47.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94cf6796ab09'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 商品マスタテーブルの作成
    op.create_table(
        'products',
        sa.Column('prd_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('code', sa.String(13), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('prd_id'),
        sa.UniqueConstraint('code')
    )

    # 取引テーブルの作成
    op.create_table(
        'transactions',
        sa.Column('trd_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('datetime', sa.DateTime(), nullable=False),
        sa.Column('emp_cd', sa.String(10), nullable=False),
        sa.Column('store_cd', sa.String(5), nullable=False),
        sa.Column('pos_no', sa.String(3), nullable=False),
        sa.Column('total_amt', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('trd_id')
    )

    # 取引明細テーブルの作成
    op.create_table(
        'transaction_details',
        sa.Column('dtl_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('trd_id', sa.Integer(), nullable=False),
        sa.Column('prd_id', sa.Integer(), nullable=False),
        sa.Column('prd_code', sa.String(13), nullable=False),
        sa.Column('prd_name', sa.String(50), nullable=False),
        sa.Column('prd_price', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['trd_id'], ['transactions.trd_id']),
        sa.ForeignKeyConstraint(['prd_id'], ['products.prd_id']),
        sa.PrimaryKeyConstraint('dtl_id')
    )


def downgrade() -> None:
    op.drop_table('transaction_details')
    op.drop_table('transactions')
    op.drop_table('products')
