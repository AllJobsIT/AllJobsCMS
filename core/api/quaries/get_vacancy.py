import graphene
from graphene_django import DjangoObjectType

from core.models.snippets.vacancy import Vacancy
from core.tasks.vacancy_task import ProcessVacancy


class VacancyNode(DjangoObjectType):
    tags = graphene.List(graphene.String)

    class Meta:
        model = Vacancy
        only_fields = ['title', 'requirements', 'responsibilities', 'cost', 'location',
                       'load', 'grade', 'full_vacancy_text_from_tg_chat']

    def resolve_tags(self: Vacancy, info):
        return self.tags.all().name


class CreateVacancyMutation(graphene.Mutation):
    class Arguments:
        full_vacancy_text = graphene.String()
        channel = graphene.String()

    create = graphene.Field(graphene.Boolean)

    @classmethod
    def mutate(cls, root, info, full_vacancy_text, channel):
        try:
            vacancy = Vacancy.objects.create(
                full_vacancy_text_from_tg_chat=full_vacancy_text,
                channel=channel
            )
            ProcessVacancy.create(input={'id': vacancy.id})
            create = True
        except BaseException as err:
            print(err)
            create = False
        return CreateVacancyMutation(create=create)


class VacancyMutation:
    create_vacancy = CreateVacancyMutation.Field()


class VacancyQuery:
    get_vacancy = graphene.List(VacancyNode)

    def resolve_get_vacancy(self, info, **kwargs):
        vacancy = Vacancy.objects.all()
        return vacancy
