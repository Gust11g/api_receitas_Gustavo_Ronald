"""add authentication profile fields

Revision ID: 2c7e0b4a1f9d
Revises: 9f9c28cf4abe
"""
from alembic import op
import sqlalchemy as sa

revision = "2c7e0b4a1f9d"
down_revision = "9f9c28cf4abe"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(sa.Column("first_name", sa.String(length=150), nullable=False, server_default=""))
        batch_op.add_column(sa.Column("last_name", sa.String(length=150), nullable=False, server_default=""))
        batch_op.add_column(sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
        batch_op.alter_column("senha", existing_type=sa.String(), type_=sa.String(length=255), existing_nullable=False)


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("is_active")
        batch_op.drop_column("last_name")
        batch_op.drop_column("first_name")
