import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class NetworkLinkDocument(Document):
    type_id = Text()

    class Index:
        name = 'network-link'


NetworkLinkDocument.init()


class NetworkLinkResource(BaseResource):
    doc_cls = NetworkLinkDocument
    doc_name = 'Network Link'
