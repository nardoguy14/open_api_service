import os

from repositories.mivilus_base_repository import MivilusBaseRepository


class OpenAiEmbeddingsRepository(MivilusBaseRepository):

    COLLECTION_NAME = "open_api_embeddings"

    def __init__(self):
        host = os.environ['MIVILUS_HOST']
        port = os.environ['MIVILUS_PORT']
        full_host = f"${host}:${port}"
        super().__init__(self.COLLECTION_NAME, full_host)
