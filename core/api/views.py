from django.http import JsonResponse
from rest_framework.views import APIView
from wagtail.documents.models import Document

from core.models.snippets import Worker
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
