"""create_data_scrape_urls

Revision ID: 314476470e33
Revises: bab82fd32dfe
Create Date: 2024-05-19 00:32:30.762237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '314476470e33'
down_revision: Union[str, None] = 'bab82fd32dfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'data_scrape_urls',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column("main_url", sa.VARCHAR(255), nullable=False),
        sa.Column("url", sa.VARCHAR(512), nullable=False),
        sa.Column("text", sa.TEXT, nullable=False),
        sa.Column("embeddings_type", sa.VARCHAR(255)),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
        sa.Column('modified_at', sa.DateTime(), nullable=False, server_default=func.now())
    )


def downgrade() -> None:
    op.drop_table('data_scrape_urls')
