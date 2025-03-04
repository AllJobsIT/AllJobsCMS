import graphene

from core.api.nodes.worker import WorkerType
from core.models.snippets import Worker


# Query
class WorkerQuery:
    worker_by_uuid = graphene.Field(WorkerType, uuid=graphene.String(required=True))

    def resolve_worker_by_uuid(self, info, uuid):
        try:
            return Worker.objects.get(code=uuid)
        except Worker.DoesNotExist:
            return None
