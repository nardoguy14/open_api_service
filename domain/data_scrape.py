from pydantic import BaseModel
from typing import Optional

class Job(BaseModel):
    href: str
    depth: int
    parent: Optional[str]

    def __hash__(self):
        return hash((self.href))

    def __eq__(self, other):
        if not isinstance(other, Job):
            return False
        return self.href == other.href


class DataScrapeJob(BaseModel):
    url: str
    embeddings_type: str
    max_depth: int


class DataScrapeResult(BaseModel):
    url: str
    content: str
