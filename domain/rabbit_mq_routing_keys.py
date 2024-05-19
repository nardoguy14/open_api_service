from enum import Enum


class RabbitmqRoutingKeys(Enum):
    CREATE_DATA_SCRAPE = "CREATE_DATA_SCRAPE"
    CREATE_EMBEDDINGS  = "CREATE_EMBEDDINGS"
