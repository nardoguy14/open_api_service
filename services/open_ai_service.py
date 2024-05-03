import os

import tiktoken
from openai import OpenAI

from domain.open_ai import Embedding
from repositories.open_ai_embeddings_repository import OpenAiEmbeddingsRepository


class OpenAiService():

    EMBEDDING_MODEL = "text-embedding-ada-002"
    GPT_MODEL = "gpt-3.5-turbo"
    OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY")

    def __init__(self):
        self.open_ai_repository = OpenAiEmbeddingsRepository()
        self.open_ai_client = OpenAI(api_key=self.OPEN_AI_KEY)

    def get_embedding_from_open_ai(self, query: str) -> list[float]:
        """
        Function to call OpenAI embeddings API and return back a vector representing the embedding.

        :param query: The text we want to derive an embedding from
        :return: list[float] representing the embedding
        """
        query_embedding_response = self.open_ai_client.embeddings.create(
            model=self.EMBEDDING_MODEL,
            input=query,
        )
        query_embedding = query_embedding_response.data[0].embedding
        return query_embedding

    def create_embedding(self, embedding: Embedding, create_embeddings: bool=False):
        token_count = self.get_num_of_tokens(embedding.text, self.EMBEDDING_MODEL)
        if create_embeddings:
            embedding.vector = self.get_embedding_from_open_ai(embedding.text)
        else:
            embedding.vector = [0.0 for i in range(1536)]
        result = self.open_ai_repository.insert([embedding.dict(exclude_none=True)])
        return result, token_count

    def get_related_embeddings(self, embedding, filter_param, output_fields=None):
        return self.open_ai_repository.search([embedding], filter_param, output_fields=output_fields)

    def get_embedding_by_url(self, url):
        return self.open_ai_repository.query(filter=f'$meta["url"] == "{url}"', limit=10)

    def get_num_of_tokens(self, text: str, model: str) -> int:
        """
            Return the number of tokens in a string.
            This helps when knowing ho wmuch data we can pass to ChatGPT APIs since there are
            limits on the maount of tokens that can be provided to ChatGPT.

            :param text: The text we want to calculate number of tokens for
            :param model: Model we will cal from which we want to calculate tokens for
            :return: int Number representing amount of tokens given text and model
        """
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

    def generate_query_message(
            self,
            query: str,
            prior_knowledge: list[str],
            intro: str,
            seperator: str,
            model: str,
            token_budget: int
    ) -> str:
        question = f"\n\nQuestion: {query}"
        message = intro
        for string in prior_knowledge:
            next_article = f'\n\n{seperator}:\n"""\n{string}\n"""'
            if (
                    self.get_num_of_tokens(message + next_article + question, model=model)
                    > token_budget
            ):
                break
            else:
                message += next_article
        return message + question

    def ask_chatgpt_question(
            self,
            query: str,
            intro: str,
            seperator: str,
            prior_knowledge: list[str],
            model: str = GPT_MODEL,
            token_budget: int = 4096 - 500,
    ) -> str:
        """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
        message = self.generate_query_message(query, prior_knowledge=prior_knowledge, intro=intro, seperator=seperator,
                                              model=model, token_budget=token_budget)
        messages = [
            {"role": "system", "content": "You answer questions about Covered California Health Insurnace."},
            {"role": "user", "content": message},
        ]
        response = self.open_ai_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        response_message = response.choices[0].message.content
        return response_message

