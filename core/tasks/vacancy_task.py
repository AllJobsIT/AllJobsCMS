import json
import os
import re

from aiogram.utils.formatting import Bold, Italic, Text, HashTag
from django.apps import apps
from django.db import transaction
from openai import Client

from core.models.snippets.base import Grade, Specialization
from core.models.snippets.message_settings import MessageSettings
from core.tasks import AllJobsBaseTask
from libs.bot import create_bot, create_dispatcher, loop
from libs.json import json_to_dict


class SendVacancy(AllJobsBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 1
    name = 'process_vacancy'
    actions = ['send_vacancy']

    def get_prompt(self, text, data):
        prompt = (
            f"На вход есть шаблон сообщения. Нужно оформить текст по шаблону из переменных в формате JSON.\n"
            f"Необходимо учесть, что в итоговом тексте должен быть только текст, сгенерированный по шаблону с "
            f"использованием ТОЛЬКО ТЕХ переменных, что есть в шаблоне. Шаблон текста: {text}\n\n"
            f"Переменные в формате JSON: {data}"
        )
        return prompt

    def init_bot(self):
        self.bot = create_bot()
        self.dp = create_dispatcher(self.bot, loop)
        self.channel = os.getenv('CHANNEL')

    def analize_text(self, text):
        list_texts = []
        hashtag_pattern = re.compile(r'#(\w+)')
        for line in text.splitlines():
            if "**" in line:
                list_texts.append(Bold(line.replace("**", "")))
            elif "*" in line:
                list_texts.append(Italic(line.replace("*", "")))
            elif "#" in line:
                hashtags = hashtag_pattern.findall(line)
                if hashtags:
                    for tag in hashtags:
                        list_texts.append(HashTag(f"{tag} "))
                else:
                    list_texts.append(line)
            list_texts.append("\n")

        return Text(*list_texts)

    def send_vacancy(self):
        self.init_bot()
        vacancy_id = self.task.input.get('id')
        vacancy = apps.get_model("core.Vacancy").objects.get(id=vacancy_id)
        template_message = MessageSettings.objects.all().first().text
        data = {
            "title": vacancy.title,
            "requirements": [item.value for item in vacancy.requirements],
            "responsibilities": [item.value for item in vacancy.responsibilities],
            "stack": [item.value for item in vacancy.stack],
            "cost": vacancy.cost,
            "location": vacancy.location.name,
            "load": vacancy.load,
            "tags": " ".join([f"#{tag.name}" for tag in vacancy.tags.all()]),
            "grades": [item.value.title for item in vacancy.grades],
        }
        json_data = json.dumps(data)
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "Ты продвинутый генератор текста"
                 },
                {"role": "user",
                 "content": self.get_prompt(template_message, json_data)},
            ]
        )
        result_message = response.choices[0].message.content
        new_text = self.analize_text(result_message)
        loop.run_until_complete(self.bot.send_message(self.channel, new_text.as_markdown()))
        print(f'Sent vacancy {new_text}')
        vacancy.save()


class ProcessVacancy(AllJobsBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 1
    name = 'process_vacancy'
    actions = ['process_vacancy']

    def get_prompt(self, text):
        prompt = (
            "Выдели из содержимого этого текста только следующую информацию: заголовок (title) - специализация ("
            "specialization) - технический стэк в виде массива строк (stack) - "
            "требования в виде массива строк (requirements) - обязанности в виде массива строк (responsibilities) - "
            "стоимость/рейт числом (cost) - локация, в формате числового кода страны (location) - "
            "загрузка/нагрузка (load) - тэги в виде массива строк (tags) - грейд/грейды в виде массива строк (grades)."
            "Оформи эти данные в JSON, где данные в скобках это ключи для JSON с, если каких-то значений не хватает, "
            f"то заполни их null. следуй строго по шаблону. Сам текст: {text}"
        )
        return prompt

    def process_vacancy(self):
        vacancy_id = self.task.input.get('id')
        instance = apps.get_model("core.Vacancy").objects.get(id=vacancy_id)
        try:
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "Ты продвинутый анализатор текста"
                     },
                    {"role": "user",
                     "content": self.get_prompt(instance.full_vacancy_text_from_tg_chat)}
                ]
            )
            ai_response_content = response.choices[0].message.content
            ai_response_dict = json_to_dict(ai_response_content)
            with transaction.atomic():
                instance.title = ai_response_dict.get('title', None)
                instance.requirements = [{"type": "requirements_item", "value": item} for item in
                                         ai_response_dict.get("requirements", None)]
                instance.responsibilities = [{"type": "responsibilities_item", "value": item} for item in
                                             ai_response_dict.get("responsibilities", None)]
                instance.stack = [{"type": "stack_item", "value": item} for item in
                                  ai_response_dict.get("stack", None)]
                instance.cost = ai_response_dict.get('cost', None)
                instance.location = ai_response_dict.get('location', None)
                instance.load = ai_response_dict.get('load', None)
                grades = Grade.objects.filter(title__in=ai_response_dict.get("grades", None))
                if grades:
                    instance.grades = [{"type": "grade", "value": item.id} for item in grades]
                specializations = Specialization.objects.filter(title__in=ai_response_dict.get("specialization", None))
                if specializations:
                    instance.specialization = [{"type": "specialization", "value": item.id} for item in specializations]
                for tag in ai_response_dict['tags']:
                    instance.tags.add(tag)
                instance.status += 1
        except BaseException as e:
            instance.status = -1
        instance.save()
