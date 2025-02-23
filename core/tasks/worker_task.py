import os
from datetime import datetime

from django.db import transaction
from openai import Client

from core.choices.worker import WorkerProcessStatusChoice
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
            "name": "Имя",
            "last_name": "Фамилия",
            "surname": "Отчество",
            "telegram_nickname": "telegram",
            "employer": "Работодатель",
            "grade": ["Грейды работника, например Junior, Middle"],
            "specialization": ["Специализация работника"],
            "stack": ["Стэк работника"],
            "skills": ["Навыки работника"],
            "programming_languages": ["Языки программирования"],
            "technologies": ["Используемые технологии"],
            "databases": ["Базы данных"],
            "software_development": ["Средства разработки ПО (IDE)"],
            "other_technologies": ["Остальные технологии, которые не относятся к прошлым"],
            "about_worker": "Краткое описание кандидата и его сильных сторон",
            "experience": Стаж в годах в формате float, например 4.5,
            "city": "Город",
            "citizenship": "Гражданство в виде кода страны (например, RU)",
            "english_grade": [{"Код языка (EN, RU и т.д.)": "Уровень владения (например, B2, родной)"}],
            "education": "Образование",
            "certificates": ["Сертификаты"],
            "employer_contact": "Контакт работодателя",
            "worker_contact": [{"тип": "контакт"}], # Например [{"email": "example@example.com"}, {"tel": "+7999999999999"}],
            "example_of_work": ["Ссылки на примеры работ"],
            "work_experience": [{
                "company_name": "Название компании или проекта",
                "start_year": "Начало работы (формат: MM.YYYY, если нет месяца — 01.YYYY)",
                "end_year": "Окончание работы (формат: MM.YYYY, если работает по настоящее время — текущая дата)",
                "position": "Позиция в компании",
                "description": "Описание обязанностей, задач и достижений",
                "technologies": ["Используемые технологии"]
            }],
            "links": [{"тип": "ссылка"}], # Например [{"linkedin": "https://linkedin.com/in/example"}, {"github": "https://github.com/example"}],
        }"""

        prompt = (
            "Извлеки из текста только указанную информацию и оформи её строго в JSON-формате по заданному шаблону. "
            "Не добавляй пояснений, комментариев или лишних данных. "
            "Если каких-то значений нет, заполни их значениями по умолчанию (str = '', список = [], float = 0.0, int = 0). "
            f"Текущая дата: {datetime.now().strftime('%m.%Y')}. "
            "Игнорируй нерелевантные части текста. "
            "Анализируй информацию объективно, без домыслов и догадок. "
            "Соблюдай точную структуру JSON-шаблона.\n\n"
            f"Шаблон JSON:\n{template}\n\n"
            f"Содержимое файла:\n{file_data}"
        )
        return prompt

    def get_ai_comment(self, instance, resume_data):
        prompt = f"""
        Как эксперт по найму, проанализируй следующие данные резюме и оцени уровень кандидата по каждому навыку.  

        Данные резюме:
        {resume_data}

        Если доступны, проанализируй личный сайт кандидата и его публичные репозитории на GitHub/GitLab для получения дополнительных сведений.  

        Требуется:  
        1. Оценка уровня владения каждым навыком (например, Python — Middle, Django — Senior).  
        2. Основные сильные и слабые стороны кандидата.  
        3. Рекомендации по улучшению.  

        Формат вывода:  

        - Оценка навыков:  
          - skill: grade
          ...  

        - Наблюдения:  
          - Наблюдение или рекомендация  
          ...  

        Выведи только оценки, наблюдения и рекомендации, а так же анализ открытых проектов и ссылки на их репозитории.
        Без введения, пояснений и комментариев.  
        """
        try:
            client = Client(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "Ты эксперт по найму. Анализируешь резюме"
                     },
                    {"role": "user",
                     "content": prompt}
                ]
            )
            instance.ai_comment = response.choices[0].message.content
        except BaseException as err:
            raise Exception(f"Error: {err}")
        instance.save()


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

    def _date_to_months(self, date):
        month, year = map(int, date.split('.'))
        return year * 12 + month

    def _update_work_experience(self, work_experience, instance):
        for item in work_experience:
            item.update({"worker": instance})
            if item.get("end_year"):
                item["end_year"] = datetime.strptime(str(item["end_year"]), "%m.%Y")
            if item.get("start_year"):
                item["start_year"] = datetime.strptime(str(item["start_year"]), "%m.%Y")
            total_days = item['end_year'] - item['start_year']
            item['duration'] = round(total_days.days / 365, 2)
            item["technologies"] = self._get_items(item, "technologies", "technology_item")
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
                     "content": "Ты опытный анализатор текста резюме, способный выделить из него всю необходимую "
                                "информацию и оформить ее в JSON-формате. "
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
                instance.process_status = WorkerProcessStatusChoice.MODERATION
        except BaseException as err:
            instance.process_status = WorkerProcessStatusChoice.PROCESS_ERROR
            instance.save()
            raise Exception(f"Error: {err}")
        instance.save()
        self.get_ai_comment(instance, result)
