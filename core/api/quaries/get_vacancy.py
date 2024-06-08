import graphene
from g4f.client import Client
from graphene_django import DjangoObjectType

from core.models.snippets.vacancy import Vacancy
from libs.integer import string_to_integer
from libs.json import json_to_dict


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

    create = graphene.Field(graphene.Boolean)

    @classmethod
    def mutate(cls, root, info, full_vacancy_text):
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Ты продвинутый анализатор текста, который может подчерпнуть из любого текста главную "
                            "информацию. Всё общение ты должен вести на русском языке!"
                 },
                {"role": "user",
                 "content": "Ты должен отвечать только в формате json, без лишних слов\n"
                            "Переменные в json должны соответствовать данным переменным:\n\n"
                            "title, requirements, responsibilities, cost, location, load, tags, grade\n\n"
                            "Если какого то из переменных нет, то оставляй пустую строку!\n"
                            "Если там есть локация, то проанализируй, что это за страна и в ответе запиши ее "
                            "код(Россия - RU и тд) иначе оставляй пустую строку!\n"
                            "Если в каком то моменте ты видишь, что идет перечисление чего либо, то между каждым "
                            "элементом перечисления ставь символ ';', чтобы я понимал, что это перечисление не считая tags, они всегда в виде СПИСКА!\n\n"
                            "Так же не сокращай текст, а используй его именно так, как он записан в исходном сообщении!\n"
                            f"Проанализируй следующий текст и разбей его на json так, "
                            f"чтобы было понятно, где что находится:\n\n{full_vacancy_text}"}
            ]
        )
        ai_response_content = response.choices[0].message.content
        try:
            ai_response_dict = json_to_dict(ai_response_content)
            vacancy = Vacancy.objects.create(
                full_vacancy_text_from_tg_chat=full_vacancy_text,
                title=ai_response_dict['title'] if ai_response_dict['title'] else None,
                requirements=ai_response_dict['requirements'] if ai_response_dict['requirements'] else None,
                responsibilities=ai_response_dict['responsibilities'] if ai_response_dict[
                    'responsibilities'] else None,
                cost=string_to_integer(ai_response_dict['cost']) if ai_response_dict['cost'] else None,
                location=ai_response_dict['location'] if ai_response_dict['location'] else None,
                load=ai_response_dict['load'] if ai_response_dict['load'] else None,
            )
            for tag in ai_response_dict['tags']:
                vacancy.tags.add(tag)
            vacancy.save()
            create = True
        except BaseException as err:
            print(err)
            create = False
        return CreateVacancyMutation(create=create)


class VacancyMutation:
    get_vacancy = graphene.List(VacancyNode)
    create_vacancy = CreateVacancyMutation.Field()

    def resolve_get_vacancy(self, info, **kwargs):
        vacancy = Vacancy.objects.all()
        return vacancy
