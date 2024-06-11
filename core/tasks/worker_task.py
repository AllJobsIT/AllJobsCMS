from g4f.client import Client

from core.models.snippets import Worker
from core.tasks import KITBaseTask


class ProcessVacancy(KITBaseTask):
    DEFAULT_ATTEMPT_PERIOD = 1
    name = 'process_vacancy'
    actions = ['process_worker']

    def process_worker(self):
        worker_id = self.task.input.get("id")
        instance = Worker.objects.get(id=worker_id)
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
