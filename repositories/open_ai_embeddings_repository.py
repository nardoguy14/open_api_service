from repositories.mivilus_base_repository import MivilusBaseRepository


class OpenAiEmbeddingsRepository(MivilusBaseRepository):

    COLLECTION_NAME = "open_api_embeddings"

    def __init__(self, host="http://localhost:19530"):
        super().__init__(self.COLLECTION_NAME, host)

