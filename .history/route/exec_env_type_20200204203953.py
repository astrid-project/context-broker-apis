import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class ExecEnvTypeDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env-type'


ExecEnvDocument.init()


class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
