from string import Template

import requests
from django.db import transaction
from g4f.client import Client

from core.models.snippets.message_settings import MessageSettings
from core.models.snippets.vacancy import Vacancy
from core.tasks import KITBaseTask
from libs.integer import string_to_integer
from libs.json import json_to_dict
from libs.rich_text import richtext_to_md2


class ProcessVacancy(KITBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 0.1
    name = 'process_vacancy'
    actions = ['process_vacancy', "send_vacancies"]

    def send_vacancies(self):
        all_vacancy = Vacancy.objects.filter(status=2, is_send=False).order_by('-created_at')
        for vacancy in all_vacancy:
            template_message = Template(MessageSettings.objects.all().first().text)
            data = {
                "title": vacancy.title,
                "requirements": vacancy.requirements,
                "responsibilities": vacancy.responsibilities,
                "cost": vacancy.cost,
                "location": vacancy.location,
                "load": vacancy.load,
                "tags": " ".join([f"#{tag.name}" for tag in vacancy.tags.all()]),
                "grade": vacancy.grade,
            }
            requests.post("http://127.0.0.1:8000/vacancy/",
                          json={"vacancy_text": richtext_to_md2(template_message.substitute(data))})
            vacancy.status += 1
            vacancy.save()

    def process_vacancy(self):
        vacancy_id = self.task.input.get('id')
        instance = Vacancy.objects.get(id=vacancy_id)
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
                            f"чтобы было понятно, где что находится:\n\n{instance.full_vacancy_text_from_tg_chat}"}
            ]
        )
        ai_response_content = response.choices[0].message.content
        ai_response_dict = json_to_dict(ai_response_content)
        with transaction.atomic():
            instance.title = ai_response_dict.get('title', None)
            instance.requirements = ai_response_dict.get('requirements', None),
            instance.responsibilities = ai_response_dict.get('responsibilities', None),
            instance.cost = string_to_integer(ai_response_dict['cost']) if ai_response_dict.get('cost') else None,
            instance.location = ai_response_dict.get('location', None),
            instance.load = ai_response_dict.get('load', None),
            for tag in ai_response_dict['tags']:
                instance.tags.add(tag)
            instance.status += 1
        instance.save()
