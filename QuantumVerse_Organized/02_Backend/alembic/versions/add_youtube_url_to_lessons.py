"""add youtube_url to lessons

Revision ID: add_youtube_url
Revises:
Create Date: 2026-09-12
"""

from alembic import op
import sqlalchemy as sa


revision = "add_youtube_url"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "lessons",
        sa.Column(
            "youtube_url",
            sa.String(length=500),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("lessons", "youtube_url")
