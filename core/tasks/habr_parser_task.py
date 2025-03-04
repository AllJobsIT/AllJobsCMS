import re
import urllib
from types import SimpleNamespace

import requests
from fake_useragent import UserAgent

from core.choices.worker import WorkerInputMethod, WorkerProcessStatusChoice
from core.models import Worker, Grade, Specialization, WorkExperience
from core.tasks import AllJobsBaseTask


class ProcessHabr(AllJobsBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 1
    name = 'process_habr'
    actions = ['process_habr']

    def _get_items(self, data: list, key, item_type):
        return [{"type": item_type, "value": item[key]} for item in data]

    def _get_nested_items(self, data, key, item_type):
        return [{"type": item_type, "value": {"link": value, "type": k}} for item in data.get(key, []) for k, value in
                item.items()]

    def _get_language_grade_items(self, data: list):
        return [{"type": "language",
                 "value": {"grade": item['title'].split(' ')[1], "language": item['title'].split(' ')[0]}} for item in
                data]

    def _get_filtered_items(self, model, titles, item_type):
        items = model.objects.filter(title__in=titles)
        return [{"type": item_type, "value": item.id} for item in items]

    def experience_to_days(self, experience_str):
        pattern = r'(\d+)\s*(лет|года|год|месяца|месяцев|месяц)'
        total_days = 0
        matches = re.findall(pattern, experience_str)
        for amount, unit in matches:
            amount = int(amount)
            if 'год' in unit:
                total_days += amount * 365
            elif 'месяц' in unit:
                total_days += amount * 30
        years = round(total_days / 365, 2)
        return years

    def _update_work_experience(self, work_experience, instance):
        for item in work_experience:
            experience = self.experience_to_days(item['experience'])
            new_item = {"worker": instance, 'company_name': item['companyName'],
                        'duration': experience}
            WorkExperience(**new_item).save()

    def _get_page(self, url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def process_habr(self):
        ua = UserAgent()
        base_url = "https://career.habr.com"
        base_path = "/api/frontend/resumes"
        filters_by_specialization = [2, 3, 82, 4, 72, 5, 6, 75, 1, 5, 6, 75, 1, 84, 83, 7, 77, 73, 85, 8, 86,
                                     178, 106, 98, 41, 42, 99,
                                     16843, 76, 96, 97, 95, 100, 133, 111]
        params = {'order': 'relevance',
                  'currency': 'RUR',
                  's[]': None}
        for specialization_filer in filters_by_specialization:
            headers = {
                'User-Agent': ua.random
            }
            params['s[]'] = specialization_filer
            url_params = urllib.parse.urlencode(params)
            full_url = f"{base_url}{base_path}?{url_params}"
            response = requests.get(full_url, headers=headers)
            response_list = response.json()
            if response_list['list']:
                for item in response_list['list']:
                    item = SimpleNamespace(**item)
                    if Worker.objects.filter(unique_id=item.id).exists():
                        continue
                    worker = Worker(name=item.title, input_method=WorkerInputMethod.HABR, unique_id=item.id)
                    worker.employer = item.lastJob.get('company', None)['title'] if item.lastJob else None
                    worker.education = f"{item.education.get('university', None)['title']} {item.education.get('faculty', '')}" if item.education else None
                    worker.city = item.location.get('title', '') if item.location else None
                    worker.links = self._get_nested_items({"links": [{"Habr": f"{base_url}{item.href}"}]}, 'links',
                                                          'link')
                    worker.skills = self._get_items(item.skills, "title",
                                                    "skill_item") if item.skills else None
                    worker.english_grade = self._get_language_grade_items(
                        item.foreignLanguages) if item.foreignLanguages else None
                    worker.grades = self._get_filtered_items(Grade, [item.qualification['title']],
                                                             "grade") if item.qualification else None
                    worker.specialization = self._get_filtered_items(Specialization,
                                                                     [spec['title'] for spec in item.specializations],
                                                                     "specialization") if item.specializations else None
                    worker.process_status = WorkerProcessStatusChoice.MODERATION
                    worker.experience = self.experience_to_days(item.experience['title']) if item.experience else None
                    worker.save()
                    self._update_work_experience(item.companiesHistory, worker) if item.companiesHistory else None
            else:
                print(
                    f"Ошибка: Не удалось получить страницу, статус код: {response.status_code}. Текст ошибки: {response.text}")
