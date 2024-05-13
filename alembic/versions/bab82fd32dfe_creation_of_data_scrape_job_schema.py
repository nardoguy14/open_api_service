"""creation of data scrape job schema

Revision ID: bab82fd32dfe
Revises: 
Create Date: 2024-05-12 16:11:27.290929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func



# revision identifiers, used by Alembic.
revision: str = 'bab82fd32dfe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'data_scrape_jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column("url", sa.VARCHAR(255), nullable=False),
        sa.Column("max_depth", sa.Integer, nullable=False, default=1),
        sa.Column("embeddings_type", sa.VARCHAR(255)),
        sa.Column('queue_size', sa.Integer, nullable=False, default=0),
        sa.Column('sites_seen', sa.Integer, nullable=False, default=0),
        sa.Column('status', sa.VARCHAR(50)),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=func.now()),
        sa.Column('modified_at', sa.DateTime(), nullable=False, server_default=func.now())
    )


def downgrade() -> None:
    op.drop_table('data_scrape_jobs')
