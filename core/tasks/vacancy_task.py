import json
import os
import re

from aiogram.utils.formatting import Bold, Italic, Text, HashTag
from django.apps import apps
from django.db import transaction
from openai import Client

from core.choices.vacancy import VacancyProcessStatusChoices
from core.models.snippets.base import Grade, Specialization
from core.models.snippets.message_settings import MessageSettings
from core.tasks import AllJobsBaseTask
from libs.bot import create_bot, create_dispatcher, loop
from libs.json import json_to_dict


class SendVacancy(AllJobsBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 1
    name = 'send_vacancy'
    actions = ['send_vacancy']

    def get_prompt(self, text, data):
        prompt = (
            "На вход есть шаблон сообщения в формате jinja2. Нужно оформить текст по шаблону из переменных в формате JSON.\n"
            "В ответе ТОЛЬКО итоговый текст. Если какая то из переменных не указана, то пропусти ее, не считая моментов,"
            "когда есть условия if else. Если есть перечисление списка, то каждый элемент списка с новой строки."
            f"Шаблон текста: {text}\n\n"
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
            else:
                list_texts.append(line)
            list_texts.append("\n")
        return Text(*list_texts)

    def send_vacancy(self):
        self.init_bot()
        vacancy_id = self.task.input.get('id')
        try:
            vacancy = apps.get_model("core.Vacancy").objects.get(id=vacancy_id, status=3)
        except apps.get_model("core.Vacancy").DoesNotExist:
            self.task.delete()
            return
        try:
            template_message = MessageSettings.objects.all().first().text
            salary_item = vacancy.salary[0].value
            data = {
                "title": vacancy.title,
                "requirements": [item.value for item in vacancy.requirements],
                "responsibilities": [item.value for item in vacancy.responsibilities],
                "stack": [item.value for item in vacancy.stack],
                "cost": vacancy.cost,
                "salary": f"{salary_item['size']} {salary_item['currency'].symbol}",
                "location": vacancy.location.name,
                "load": vacancy.load,
                "tags": " ".join([f"#{tag.name}" for tag in vacancy.tags.all()]),
                "grades": [item.value.title for item in vacancy.grades],
            }
            json_data = json.dumps(data)
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o",
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
            vacancy.status = 4
        except BaseException as err:
            vacancy.status = 3
            raise Exception(f"Error: {err}")
        vacancy.save()


class ProcessVacancy(AllJobsBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 1
    name = 'process_vacancy'
    actions = ['process_vacancy']

    def get_prompt(self, text):
        template = """{
                    "title": Название вакансии,
                    "specialization": [Список специализаций вакансии],
                    "stack": [Список стэка вакансии],
                    "requirements": [Требования к сотруднику],
                    "responsibilities": [Обязанности сотрудника],
                    "cost": Рейт вакансии в виде числа, если исходный рейт не указан, или указан словами, то 0,
                    "location": Локация вакансии в виде числового кода страны, например RU,
                    "load": Загрузка вакансии, например fulltime/полный и тд,
                    "tags": [Тэги],
                    "grades": [Грейды требуемого работника],
                    "links": [
                        {тип ссылки: ссылка}
                    ],
                }
                """
        prompt = (
            "Выдели из содержимого этого текста, только следующую информацию и оформи эти данные в JSON, "
            f"где данные в скобках это ключи для JSON с, если каких-то значений не хватает, то заполни их null, если же"
            f" отсутствуют данные там, где должен был быть список, то оставь пустой список. Следуй "
            f"строго по шаблону, без лишних слов:\n"
            f"Шаблон:\n{template}\n\nСодержимое файла: {text}"
        )
        return prompt

    def _get_items(self, data, key, item_type):
        return [{"type": item_type, "value": item} for item in data.get(key, [])]

    def _get_filtered_items(self, model, titles, item_type):
        items = model.objects.filter(title__in=titles)
        return [{"type": item_type, "value": item.id} for item in items]

    def process_vacancy(self):
        vacancy_id = self.task.input.get('id')
        try:
            instance = apps.get_model("core.Vacancy").objects.get(id=vacancy_id)
        except apps.get_model("core.Vacancy").DoesNotExist:
            self.task.delete()
            return
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
                instance.requirements = self._get_items(ai_response_dict, "requirements", "requirements_item")
                instance.responsibilities = self._get_items(ai_response_dict, "responsibilities",
                                                            "responsibilities_item")
                instance.stack = self._get_items(ai_response_dict, "stack", "stack_item")
                instance.cost = ai_response_dict.get('cost', None)
                instance.location = ai_response_dict.get('location', None)
                instance.load = ai_response_dict.get('load', None)
                grades = ai_response_dict.get("grades", [])
                instance.grades = self._get_filtered_items(Grade, grades, "grade")

                specializations = ai_response_dict.get("specialization", [])
                instance.specialization = self._get_filtered_items(Specialization, specializations, "specialization")
                for tag in ai_response_dict['tags']:
                    instance.tags.add(tag)
                instance.status = VacancyProcessStatusChoices.MODERATION
        except BaseException as e:
            instance.status = VacancyProcessStatusChoices.PROCESS_ERROR
            raise Exception(f"Error: {e}")
        instance.save()
