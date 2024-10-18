from botmanager.models import Task
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.documents.models import Document

from core.models.snippets import Worker
from core.tasks.habr_parser_task import ProcessHabr
from core.tasks.worker_task import ProcessWorker


class ParserResumeAPIView(APIView):
    def post(self, request):
        if request.method == 'POST' and request.FILES['file']:
            uploaded_file = request.FILES['file']
            document = Document.objects.create(file=uploaded_file, title=uploaded_file.name)
            worker = Worker.objects.create(
                name='-',
                last_name='-',
                file=document,
            )
            worker.save()
            ProcessWorker.create(input={'id': worker.id})
            return JsonResponse({'message': 'File uploaded successfully'}, status=200)
        else:
            return JsonResponse({'error': 'No file was uploaded'}, status=400)


class HabrParsingStatus(APIView):
    def get(self, request):
        disable = True
        data = {"is_run": False,
                "is_failed": True,
                "disable": disable,
                "message": "Ошибка получения статуса задачи парсинга!"
                }
        try:
            task = Task.objects.get(name='process_habr')
        except Task.DoesNotExist:
            task = None
        if task:
            if task.is_failed:
                message = "Парсинг завершился с ошибкой. Обратитесь к разработчику!"
            elif task.in_process:
                message = "Парсинг Habr уже запущен."
            elif task.is_complete:
                message = "Парсинг успешно выполнился. Запустить заново?"
                disable = False
            else:
                message = "Задача создана, парсинг скоро начнется!"
        else:
            message = "Запустить парсинг с Habr."
            disable = False
        data = {
            "is_run": task.in_process,
            "is_failed": task.is_failed,
            "disable": disable,
            "message": message
        }
        return JsonResponse(status=200, data=data)

    def post(self, request):
        task = Task.objects.filter(name='process_habr').first()
        if task:
            if task.in_process:
                pass
            elif task.is_complete:
                task.is_complete = False
                task.save()
        else:
            ProcessHabr.create(is_unique=True)
        return Response(status=200)
