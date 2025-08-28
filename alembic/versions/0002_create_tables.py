"""create tables users, tools, loans

Revision ID: 0002_create_tables
Revises: 0001_create_database
Create Date: 2025-08-27 00:01:00

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as __unused  # not required but safe if installed

revision = '0002_create_tables'
down_revision = '0001_create_database'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(128), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(256), nullable=False),
        sa.Column('created_at', sa.DateTime)
    )

    op.create_table(
        'tools',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('daily_rate', sa.Float, nullable=False, default=0.0),
        sa.Column('category', sa.String(128), nullable=True),
        sa.Column('condition', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime)
    )

    op.create_table(
        'loans',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tool_id', sa.Integer, sa.ForeignKey('tools.id'), nullable=False),
        sa.Column('borrower_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('start_date', sa.Date, nullable=False),
        sa.Column('end_date', sa.Date, nullable=False),
        sa.Column('status', sa.String(32), nullable=False),
        sa.Column('total_cost', sa.Float, nullable=False, default=0.0),
        sa.Column('created_at', sa.DateTime)
    )

def downgrade():
    op.drop_table('loans')
    op.drop_table('tools')
    op.drop_table('users')
