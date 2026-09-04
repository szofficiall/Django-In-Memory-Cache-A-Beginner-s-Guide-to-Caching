from django.urls import path
from . import views

urlpatterns = [
    path("users_list/", views.users_list, name="users_list"),
]
