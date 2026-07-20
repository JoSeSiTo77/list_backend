from django.urls import path
from .views import get_tasks, save_tasks, delete_task, update_task

urlpatterns = [
    path('save/', save_tasks, name='save'),
    path('list/', get_tasks, name='list'),
    path('delete/', delete_task, name='delete'),
    path('update/', update_task, name='delete'),
]