import os

from repositories.mivilus_base_repository import MivilusBaseRepository


class OpenAiEmbeddingsRepository(MivilusBaseRepository):

    COLLECTION_NAME = "open_api_embeddings"

    def __init__(self):
        host = os.environ['MIVILUS_HOST']
        port = os.environ['MIVILUS_PORT']
        full_host = f"{host}:{port}"
        super().__init__(full_host, self.COLLECTION_NAME)
        if not self.client.has_collection(self.COLLECTION_NAME):
            self.client.create_collection(
                collection_name="open_api_embeddings",
                dimension=1536,
                auto_id=True
            )
