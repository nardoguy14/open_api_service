from fastapi import APIRouter, Query

from app.domain.open_ai import EmbeddingsCreationResponse, ChatGptQuestionReq, Embedding
from app.services.open_ai_service import OpenAiService
from app.util.embeddings.embeddings_producer import EmbeddingsProducer

open_ai_router = APIRouter()
open_ai_service = OpenAiService()

@open_ai_router.post("/openapi/embeddings")
def get_embeddings(embedding: Embedding, create_embeddings: bool = Query(False)):
    result, tokens = open_ai_service.create_embedding(embedding, create_embeddings)
    return EmbeddingsCreationResponse(ids=list(result['ids']), token_count=tokens)

@open_ai_router.post("/openapi/embeddings/{embeddings_type}")
def get_embeddings(embeddings_type: str, create_embeddings: bool = Query(False)):
    producer = EmbeddingsProducer()
    producer.send_embeddings_job({
        'embeddings_type': embeddings_type,
        'create_embeddings': create_embeddings
    })

@open_ai_router.post("/openapi/questions/response")
def create_question(question: ChatGptQuestionReq):
    filter = f'$meta["embeddings_type"] == "{question.embeddings_type}"'
    embedding_of_query = open_ai_service.get_embedding_from_open_ai(question.query)
    embeddings_search_result = open_ai_service.get_related_embeddings(embedding=embedding_of_query, filter_param=filter, output_fields=['text', 'url'])
    texts = []
    for i in embeddings_search_result[0]:
        print(i)
        texts.append(i['entity']['text'])
    response = open_ai_service.ask_chatgpt_question(query=question.query,
    intro=question.intro,
    seperator=question.seperator,
    prior_knowledge=texts,
    model=open_ai_service.GPT_MODEL,
    token_budget=5000)
    return {
        'response_message': response,
        'related_messages': embeddings_search_result
    }
