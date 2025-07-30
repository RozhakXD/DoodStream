from django.urls import path
from .views import DownloadAPIView, TaskStatusAPIView

urlpatterns = [
    path('download/', DownloadAPIView.as_view(), name='start-download'),
    
    path('status/<str:task_id>/', TaskStatusAPIView.as_view(), name='task-status'),
]