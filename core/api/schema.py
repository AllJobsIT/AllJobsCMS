import graphene

from core.api.quaries import VacancyMutation, VacancyQuery


class Mutation(
    graphene.ObjectType,
    VacancyMutation
):
    class Meta:
        description = "Main Mutation"


class Query(
    graphene.ObjectType,
    VacancyQuery
):
    class Meta:
        description = "Main Query"


schema = graphene.Schema(query=Query, mutation=Mutation)
