import graphene


class Query(
    graphene.ObjectType,
):
    class Meta:
        description = "Main Query"


schema = graphene.Schema(query=Query)
