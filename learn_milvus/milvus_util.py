from pymilvus import connections
from pymilvus import utility


class MilvusUtil(object):
    def __init__(self, host, port, alias='default'):
        self.alias = alias
        connections.connect(alias=alias, host=host, port=port)

    def collection_is_exist(self, collection_name):
        return utility.has_collection(collection_name, self.alias)

    def list_collection(self):
        return utility.list_collections(using=self.alias)

    def close(self):
        connections.disconnect(alias=self.alias)
