from pydantic import BaseModel
from typing import Optional

class EmbeddingsCreationResponse(BaseModel):
    ids: list[float]
    token_count: int


class ChatGptQuestionReq(BaseModel):
    query: str
    embeddings_type: str
    intro: str
    seperator: str


class Embedding(BaseModel):
    id: Optional[str]=None
    url: Optional[str]=None
    vector: Optional[list[float]]=None
    embeddings_type: str
    text: str
