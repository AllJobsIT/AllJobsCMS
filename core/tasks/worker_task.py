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
            "education": Образование,
            "certificates": [Сертификаты],
            "employer_contact": Контакт работодателя,
            "worker_contact": [{тип: контакт}] например [{"email": "example@example.com"}, {"tel": "+7999999999999"}],
            "example_of_work": [Ссылки на примеры работ],
            "work_experience": [{
                "company_name": Название компании,
                "start_year": Начало работы год числом,
                "end_year": Окончание работы год числом. Если работает по сей день, то текущий год,
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

    def process_worker(self):
        worker_id = self.task.input.get("id")
        instance = Worker.objects.get(id=worker_id)
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
                instance.name = result_dict.get('name', None)
                instance.last_name = result_dict.get('last_name', None)
                instance.surname = result_dict.get('surname', None)
                instance.telegram_nickname = result_dict.get('telegram_nickname', None)
                instance.employer = result_dict.get('employer', None)
                instance.stack = [{"type": "stack_item", "value": item} for item in
                                  result_dict.get("stack", None)]
                instance.skills = [{"type": "skill_item", "value": item} for item in
                                   result_dict.get("skills", None)]
                instance.programming_languages = [{"type": "language_item", "value": item} for item in
                                                  result_dict.get("programming_languages", None)]
                instance.technologies = [{"type": "technology_item", "value": item} for item in
                                         result_dict.get("technologies", None)]
                instance.databases = [{"type": "database_item", "value": item} for item in
                                      result_dict.get("databases", None)]
                instance.software_development = [{"type": "software_development_item", "value": item} for item in
                                                 result_dict.get("software_development", None)]
                instance.other_technologies = [{"type": "other_technology_item", "value": item} for item in
                                               result_dict.get("other_technologies", None)]
                instance.about_worker = result_dict.get('about_me', None)
                instance.experience = result_dict.get('experience', None)
                instance.city = result_dict.get('city', None)
                instance.citizenship = result_dict.get("citizenship", None)
                instance.english_grade = [{"type": "language", "value": {"grade": value, "language": key}} for item in
                                          result_dict.get('english_grade', []) for key, value in item.items()]
                instance.education = result_dict.get('education', None)
                instance.certificates = [{"type": "certificate_item", "value": item} for item in
                                         result_dict.get("certificates", None)]
                instance.employer_contact = result_dict.get('employer_contact', None)
                instance.worker_contact = [{"type": "contact", "value": {"value": value, "name": key}} for item in
                                           result_dict.get('worker_contact', []) for key, value in item.items()]
                instance.example_of_work = [{"type": "example_of_work_item", "value": item} for item in
                                            result_dict.get("example_of_work", None)]
                for item in result_dict.get("work_experience", []):
                    item.update({"worker": instance})
                    if item["end_year"]:
                        item.update({"end_year": datetime.strptime(str(item["end_year"]), "%Y")})
                    if item["start_year"]:
                        item.update({"start_year": datetime.strptime(str(item["start_year"]), "%Y")})
                    exp = WorkExperience(**item)
                    exp.save()
                instance.work_experience = result_dict.get("work_experience")
                instance.links = [{"type": "link", "value": {"link": value, "type": key}} for item in
                                  result_dict.get('links', []) for key, value in item.items()]
                grade = Grade.objects.filter(title__in=result_dict.get("grade", None))
                if grade:
                    instance.grades = [{"type": "grade", "value": item.id} for item in grade]
                specializations = Specialization.objects.filter(title__in=result_dict.get("specialization", None))
                if specializations:
                    instance.specialization = [{"type": "specialization", "value": item.id} for item in specializations]
                instance.status += 1
        except BaseException as err:
            instance.status = -1
        instance.save()
