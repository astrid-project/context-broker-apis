from marshmallow import Schema
from marshmallow.fields import Integer, List, Nested, Str


class QueryRequestOrderSchema(Schema):
    """Order the filtered items."""
    target = Str(required=True, example='name',
                 description='The field to compare.')
    mode = Str(required=True, enum=['asc', 'desc'], description='Order mode.',
               example='desc', default='asc')


class QueryRequestLimitSchema(Schema):
    """Limit the items to return."""
    _from = Integer(data_key='from', example=1,
                    description='Started index of the items to return.')
    _to = Integer(data_key='to', example=5,
                  description='Ended index of the items to return.')


class QueryRequestFilterSchema(Schema):
    """For numeric comparison in the clause."""
    target = Str(required=True, example='id',
                 description='The field to compare.')
    expr = Str(required=True, example='apache',
               description='The expression to compare to the field.')


class QueryRequestClauseSchema(Schema):
    """Represents a clause to filter a item based on various conditions."""
    _and = Nested('self', data_key='and', many=True,
                  description='All the clause has to be satisfied.')
    _or = Nested('self', data_key='or', many=True,
                 description='At least the clause has to be satisfied.')
    _not = Nested('self', data_key='not',
                  description='The clause has to be not satisfied.')
    lte = Nested(QueryRequestFilterSchema,
                 description='The target field must be lower or equal to the expr value.')
    gte = Nested(QueryRequestFilterSchema,
                 description='The target field must be greater or equal to the expr value.')
    lt = Nested(QueryRequestFilterSchema,
                description='The target field must be lower than the expr value.')
    gt = Nested(QueryRequestFilterSchema,
                description='The target field must be greater to the expr value.')
    equals = Nested(QueryRequestFilterSchema,
                    description='The target field must be equal to the expr value.')
    reg_exp = Nested(QueryRequestFilterSchema,
                     description='The target field must be satisfy the regular expression in expr.')


class QueryRequestSchema(Schema):
    """Query request to filter the items."""
    select = Str(description='Fields to return.', many=True, example='id')
    where = Nested(QueryRequestClauseSchema,
                   description='Filter the items based on different conditions.')
    order = Nested(QueryRequestOrderSchema, many=True,
                   description='Order the filtered items.')
    limit = Nested(QueryRequestLimitSchema,
                   description='Limit the number of items to return.')