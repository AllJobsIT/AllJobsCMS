import graphene

from core.api.queries import VacancyMutation, VacancyQuery
from core.api.queries.get_chats import ChatQuery
from core.api.queries.worker import WorkerQuery


class Mutation(
    graphene.ObjectType,
    VacancyMutation
):
    class Meta:
        description = "Main Mutation"


class Query(
    graphene.ObjectType,
    VacancyQuery,
    ChatQuery,
    WorkerQuery
):
    class Meta:
        description = "Main Query"


schema = graphene.Schema(query=Query, mutation=Mutation)
