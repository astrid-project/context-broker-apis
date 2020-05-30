from document.exec_env import ExecEnvDocument
from resource.base import BaseResource
from schema.exec_env import ExecEnvSchema
from docstring import docstring


@docstring(method='get',
         sum='Execution Environment Read (Single)',
         desc='Get the execution environment with the given `id` and filtered by the query in the request body.',
         resp='Execution environment with the given `id` and filtered by the query in the request body.')
@docstring(method='post',
         sum='Execution Environment Creation (Single)',
         desc='Create a new execution environment with the given `id`.',
         resp='Execution environment with the given `id` created.')
@docstring(method='delete',
         sum='Execution Environment Delete (Single)',
         desc="""Delete the execution environment with the given `id`
                 and filtered by the query in the request body.""",
         resp='Execution environment with the given `id` and filtered by the query in the request body deleted.')
@docstring(method='put',
         sum='Execution Environment Update (Single)',
         desc='Update the execution environment with the given `id`.',
         resp='Execution environment with the given `id` updated.')
class ExecEnvSelectedResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
    routes = '/exec-env/{id}'
    schema_cls =ExecEnvSchema

