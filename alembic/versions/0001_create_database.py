"""create database (ensure file exists)

Revision ID: 0001_create_database
Revises: 
Create Date: 2025-08-27 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_database'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Simply connecting will cause SQLite file to be created.
    conn = op.get_bind()
    conn.execute(sa.text("SELECT 1"))

def downgrade():
    # Can't safely remove DB file from migration.
    pass
