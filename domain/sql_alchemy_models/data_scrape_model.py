
from repositories.postgres_repository import postgres_base_repo
from sqlalchemy.sql import func

db = postgres_base_repo.db


class DataScrapeJob(db.Model):
    __tablename__ = 'data_scrape_jobs'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.VARCHAR(255), nullable=False)
    max_depth = db.Column(db.Integer, nullable=False, default=1)
    embeddings_type = db.Column(db.VARCHAR(255))
    queue_size = db.Column(db.Integer, nullable=False, default=0)
    sites_seen = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.VARCHAR(50))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    modified_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())


class DataScrapeJobUrl(db.Model):
    __tablename__ = 'data_scrape_urls'
    id = db.Column(db.Integer, primary_key=True)
    main_url = db.Column(db.VARCHAR(255), nullable=False)
    url = db.Column(db.VARCHAR(512), nullable=False)
    text = db.Column(db.Text, nullable=False)
    embeddings_type = db.Column(db.VARCHAR(255))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
    modified_at = db.Column(db.DateTime(), nullable=False, server_default=func.now())
