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
        exists = Task.objects.filter(name='process_habr', in_process=True).exists()
        return Response(status=200, data=exists)

    def post(self, request):
        if Task.objects.filter(name='process_habr', in_process=True).exists():
            pass
        else:
            ProcessHabr.create(is_unique=True)
        return Response(status=200)
