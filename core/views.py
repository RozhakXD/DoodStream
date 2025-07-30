from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import download_video_task, scrape_folder_task
import re

class HomePageView(TemplateView):
    """
    A view to render the main index.html page.
    """
    template_name = 'index.html'

def is_valid_doodstream_url(url: str) -> bool:
    """
    Validates if the URL seems to be a valid DoodStream link.
    Checks for the presence of /e/, /d/, or /f/ paths.
    This is a quick check to prevent processing invalid URLs.
    """
    if not url or not isinstance(url, str):
        return False
    
    return bool(re.search(r"/(e|d|f)/", url))

class DownloadAPIView(APIView):
    """
    API View to trigger the video download task.
    Accepts a POST request with a 'url'.
    """
    def post(self, request, *args, **kwargs):
        video_url = request.data.get('url')

        if not is_valid_doodstream_url(video_url):
            return Response(
                {"error": "URL yang dimasukkan tidak valid atau tidak didukung."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if '/f/' in video_url:
            task = scrape_folder_task.delay(video_url)
            response_data = {"task_id": task.id, "type": "folder_scrape"}
        else:
            task = download_video_task.delay(video_url)
            response_data = {"task_id": task.id, "type": "single_download"}
        
        return Response(response_data, status=status.HTTP_202_ACCEPTED)

class TaskStatusAPIView(APIView):
    """
    API View to check the status of a Celery task.
    Accepts a GET request with a 'task_id'.
    """
    def get(self, request, task_id, *args, **kwargs):
        task_result = AsyncResult(task_id)

        response_data = {
            "task_id": task_id,
            "status": task_result.status,
            "result": None
        }

        if task_result.failed():
            response_data['result'] = {'status': 'FAILURE', 'error': str(task_result.info)}
        elif task_result.successful():
            response_data['result'] = task_result.result
        elif task_result.status == 'PROGRESS':
            response_data['result'] = task_result.info

        return Response(response_data, status=status.HTTP_200_OK)