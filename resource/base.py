import falcon
from query_parser import QueryParser
import elasticsearch
from utils import *

class BaseResource(object):
    def __init__(self):
        self.__init()

    def __init(self):
        try:
            print(f'Info: start initialization index {self.doc_cls.Index.name}.')
            self.doc_cls.init()
        except:
            print(f'Error: initialization index {self.doc_cls.Index.name} not possible.')
            print(f'Info: try again.')
            self.__init()
        else:
            print(f'Success: index {self.doc_cls.Index.name} initialized')


    def on_base_get(self, req, resp, id=None):
        try:
            res = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {}), id=id
            ).execute()
            resp.media = [dict(item.to_dict(), id=item.meta.id)
                               for item in res]
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error, description=req_error.info)

    def on_base_post(self, req, resp, id=None):
        res = []
        query = req.context.get('json', [])
        if id is not None:
            if type(query) is list:
                raise falcon.HTTPBadRequest(
                    title='id provided', description=f'Request can create only 1 new {self.doc_name}')
            single = True
        else:
            single = False
        for data in wrap(query):
            data_id = data.pop('id', None)
            if data_id is None and not single:
                res.append({
                    'status': 'error',
                    'title': 'Request not valid',
                    'description': 'id property not found',
                    'http-status-code': falcon.HTTP_NOT_FOUND
                })
            elif data_id is not None and single:
                res.append({
                    'id': data_id,
                    'status': 'error',
                    'title': 'Request not valid',
                    'description': f'id={id} provided',
                    'http-status-code': falcon.HTTP_CONFLICT
                })
            else:
                try:
                    self.doc_cls.get(id=data_id)
                except elasticsearch.NotFoundError:
                    res.append({'id': data_id, 'status': self.doc_cls(
                        meta={'id': data_id}, **data).save()})
                else:
                    res.append({
                        'id': data_id,
                        'status': 'error',
                        'title': f'{self.doc_name} already found',
                        'description': f'id already present',
                        'http-status-code': falcon.HTTP_CONFLICT
                    })
        resp.media = res

    def on_base_delete(self, req, resp, id=None):
        try:
            resp.media = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {}), id=id).delete().to_dict()
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error, description=req_error.info)

    def on_base_put(self, req, resp, id=None):
        res=[]
        query = req.context.get('json', [])
        if id is not None:
            if type(query) is list:
                raise falcon.HTTPBadRequest(
                    title='id provided', description=f'Request can create only 1 new {self.doc_name}')
            single = True
        else:
            single = False
        for data in wrap(query):
            data_id = data.pop('id', None)
            if data_id is None and not single:
                res.append({
                    'status': 'error',
                    'title': 'Request not valid',
                    'description': 'id property not found',
                    'http-status-code': falcon.HTTP_NOT_FOUND
                })
                res_code = falcon.HTTP_NOT_FOUND
            elif data_id is not None and single:
                res.append({
                    'id': data_id,
                    'status': 'error',
                    'title': 'Request not valid',
                    'description': f'id={id} provided',
                    'http-status-code': falcon.HTTP_CONFLICT
                })
            else:
                try:
                    res.append(
                        {'id': data_id, 'status': self.doc_cls.get(id=data_id).update(**data)})
                except elasticsearch.NotFoundError:
                    res.append({
                        'id': data_id,
                        'status': 'error',
                        'title': f'{self.doc_name} not found',
                        'description': f'id not found',
                        'http-status-code': falcon.HTTP_NOT_FOUND
                    })
        resp.media = res
