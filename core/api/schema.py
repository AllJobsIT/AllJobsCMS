import graphene

from core.api.quaries import VacancyMutation


class Query(
    graphene.ObjectType,
    VacancyMutation
):
    class Meta:
        description = "Main Query"


schema = graphene.Schema(query=Query)
