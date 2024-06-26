import os
from datetime import datetime

from django.db import transaction
from openai import Client

from core.models.snippets import Worker, WorkExperience
from core.models.snippets.base import Grade, Specialization
from core.tasks import AllJobsBaseTask
from libs.file import load_document
from libs.json import json_to_dict


class ProcessWorker(AllJobsBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 1
    name = 'process_worker'
    actions = ['process_worker']

    def get_prompt(self, file_data):
        template = """{
            "name": Имя,
            "last_name": Фамилия,
            "surname": Отчество,
            "telegram_nickname": telegram,
            "employer": Работодатель,
            "grade": [Грейды работника, например Junior, Middle],
            "specialization": [Специализация работника]
            "stack": [Стэк работника],
            "skills": [Навыки работника],
            "programming_languages": [Языки программирования],
            "technologies": [Используемые технологии],
            "databases": [Базы данных],
            "software_development": [Средства разработки ПО(IDE)],
            "other_technologies": [Остальные технологии, которые не относятся к прошлым],
            "about_worker": О работнике,
            "experience": Стаж в виже float числа,
            "city": "Город",
            "citizenship": Гражданство в виде кода страны, например RU,
            "english_grade": [{Язык: уровень владения. Подходит как уровень владения, так и числовое представление}],
             например будут валидны варианты как {RU: B2}, так и {RU: родной},
            "education": Образование,
            "certificates": [Сертификаты],
            "employer_contact": Контакт работодателя,
            "worker_contact": [{тип: контакт}] например [{"email": "example@example.com"}, {"tel": "+7999999999999"}],
            "example_of_work": [Ссылки на примеры работ],
            "work_experience": [{
                "company_name": Название компании,
                "start_year": Начало работы год числом,
                "end_year": Окончание работы год числом. Если работает по сей день, то текущий год,
                "duration": Срок работы в виде float числа, например 4.2,
                "position": Позиция в компании,
                "description": Описание,
            }],
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
            f"Шаблон:\n{template}\n\nСодержимое файла: {file_data}"
        )
        return prompt

    def _get_items(self, data, key, item_type):
        return [{"type": item_type, "value": item} for item in data.get(key, [])]

    def _get_nested_items(self, data, key, item_type):
        return [{"type": item_type, "value": {"value": value, "name": k}} for item in data.get(key, []) for k, value in
                item.items()]

    def _get_language_grade_items(self, data, key):
        return [{"type": "language", "value": {"grade": value, "language": k}} for item in data.get(key, []) for
                k, value in item.items()]

    def _get_filtered_items(self, model, titles, item_type):
        items = model.objects.filter(title__in=titles)
        return [{"type": item_type, "value": item.id} for item in items]

    def _update_work_experience(self, work_experience, instance):
        for item in work_experience:
            item.update({"worker": instance})
            if item.get("end_year"):
                item["end_year"] = datetime.strptime(str(item["end_year"]), "%Y")
            if item.get("start_year"):
                item["start_year"] = datetime.strptime(str(item["start_year"]), "%Y")
            WorkExperience(**item).save()

    def process_worker(self):
        worker_id = self.task.input.get("id")
        try:
            instance = Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist:
            self.task.delete()
            return
        try:
            data = load_document(instance.file.file.path)
            client = Client(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "Ты продвинутый анализатор текста"
                     },
                    {"role": "user",
                     "content": self.get_prompt(data[0].page_content)}
                ]
            )
            result = response.choices[0].message.content
            result_dict = json_to_dict(json_message=result)
            with transaction.atomic():
                instance.name = result_dict.get('name')
                instance.last_name = result_dict.get('last_name')
                instance.surname = result_dict.get('surname')
                instance.telegram_nickname = result_dict.get('telegram_nickname')
                instance.employer = result_dict.get('employer')
                instance.stack = self._get_items(result_dict, "stack", "stack_item")
                instance.skills = self._get_items(result_dict, "skills", "skill_item")
                instance.programming_languages = self._get_items(result_dict, "programming_languages", "language_item")
                instance.technologies = self._get_items(result_dict, "technologies", "technology_item")
                instance.databases = self._get_items(result_dict, "databases", "database_item")
                instance.software_development = self._get_items(result_dict, "software_development",
                                                                "software_development_item")
                instance.other_technologies = self._get_items(result_dict, "other_technologies",
                                                              "other_technology_item")
                instance.about_worker = result_dict.get('about_me')
                instance.experience = result_dict.get('experience')
                instance.city = result_dict.get('city')
                instance.citizenship = result_dict.get("citizenship")
                instance.english_grade = self._get_language_grade_items(result_dict, 'english_grade')
                instance.education = result_dict.get('education')
                instance.certificates = self._get_items(result_dict, "certificates", "certificate_item")
                instance.employer_contact = result_dict.get('employer_contact')
                instance.worker_contact = self._get_nested_items(result_dict, 'worker_contact', 'contact')
                instance.example_of_work = self._get_items(result_dict, "example_of_work", "example_of_work_item")
                self._update_work_experience(result_dict.get("work_experience", []), instance)
                instance.links = self._get_nested_items(result_dict, 'links', 'link')
                instance.grades = self._get_filtered_items(Grade, result_dict.get("grade", []), "grade")
                instance.specialization = self._get_filtered_items(Specialization,
                                                                   result_dict.get("specialization", []),
                                                                   "specialization")
                instance.process_status = 1
        except BaseException as err:
            instance.process_status = -1
            raise Exception(f"Error: {err}")
        instance.save()
