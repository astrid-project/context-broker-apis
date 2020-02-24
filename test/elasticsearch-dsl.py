from elasticsearch_dsl import connections, Search

connections.create_connection(hosts=args.es_endpoint, timeout=args.es_timeout)

s = Search()
s = s.query('term', **{'exec-env._id': 'x4fgctkm4MXQOUHYjIag'})
res = s.execute()
print([dict(item.to_dict(), id=item.meta.id) for item in res])