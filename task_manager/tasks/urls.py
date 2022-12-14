from django.urls import path
from tasks.views import CreateTaskView, UpdateTaskView, DeleteTaskView, index


urlpatterns = [
    path('', index, name='tasks'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
]