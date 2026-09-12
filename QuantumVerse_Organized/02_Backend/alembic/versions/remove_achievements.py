"""Remove achievement feature tables.

Revision ID: remove_achievements
Revises: add_youtube_url
"""

from alembic import op


revision = "remove_achievements"
down_revision = "add_youtube_url"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("user_achievements")
    op.drop_table("achievements")


def downgrade():
    # Achievement feature was intentionally removed.
    # Recreating the original tables would require restoring
    # the removed SQLAlchemy models and seed data.
    pass
