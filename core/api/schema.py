import graphene

from core.api.quaries import VacancyMutation, VacancyQuery
from core.api.quaries.get_chats import ChatQuery


class Mutation(
    graphene.ObjectType,
    VacancyMutation
):
    class Meta:
        description = "Main Mutation"


class Query(
    graphene.ObjectType,
    VacancyQuery,
    ChatQuery
):
    class Meta:
        description = "Main Query"


schema = graphene.Schema(query=Query, mutation=Mutation)
