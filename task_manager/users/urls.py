from django.urls import path
from users import views

urlpatterns = [
    path('', views.users_page, name='users'),
]
