from pymilvus import MilvusClient, DataType


class MivilusBaseRepository():

    def __init__(self, collection_name, host):
        self.client = MilvusClient(uri=host)
        self.collection_name = collection_name

    def insert(self, data):
        res = self.client.insert(
            collection_name=self.collection_name,
            data=data
        )
        return res

    def search(self, query_vectors, filter_param: str = "", limit=3, output_fields=None):
        res = self.client.search(
            collection_name=self.collection_name,     # target collection
            data=query_vectors,                # query vectors,
            filter=filter_param,
            limit=limit,                           # number of returned entities
            output_fields=output_fields
        )
        return res

    def query(self, filter=None, output_fields=None, limit=10):
        res = self.client.query(
            collection_name=self.collection_name,
            filter=filter,
            output_fields=output_fields,
            limit=limit
        )
        return res