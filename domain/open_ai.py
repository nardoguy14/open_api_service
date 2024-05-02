from pydantic import BaseModel


class EmbeddingsRequest(BaseModel):
    text: str


class EmbeddingsCreationResponse(BaseModel):
    ids: list[float]
    token_count: int


class ChatGptQuestionReq(BaseModel):
    query: str
    embeddings_type: str
    intro: str
    seperator: str
