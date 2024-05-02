from fastapi import APIRouter

from domain.open_ai import EmbeddingsRequest, EmbeddingsCreationResponse, ChatGptQuestionReq
from services.open_ai_service import OpenAiService

open_ai_router = APIRouter()
open_ai_service = OpenAiService()

@open_ai_router.post("/openapi/embeddings/type/{embeddings_type}")
def get_embeddings(embeddings_type, data: EmbeddingsRequest):
    result, tokens = open_ai_service.create_embedding(data.text, embeddings_type)
    return EmbeddingsCreationResponse(ids=list(result['ids']), token_count=tokens)

@open_ai_router.post("/openapi/questions/response")
def create_question(question: ChatGptQuestionReq):
    filter = f'$meta["embeddings_type"] == "{question.embeddings_type}"'
    embedding_of_query = open_ai_service.get_embedding_from_open_ai(question.query)
    embeddings_search_result = open_ai_service.get_related_embeddings(embedding=embedding_of_query, filter_param=filter, output_fields=['text'])
    texts = []
    for i in embeddings_search_result[0]:
        texts.append(i['entity']['text'])
    response = open_ai_service.ask_chatgpt_question(query=question.query,
    intro=question.intro,
    seperator=question.seperator,
    prior_knowledge=texts,
    model=open_ai_service.GPT_MODEL,
    token_budget=5000)
    return response
