from django.urls import path
from . import views

from .views import (
    TodoListApiView,
)

urlpatterns = [
    path("json", views.index),
    path("", TodoListApiView.as_view(), name="index"),
    path("render",  views.renderHTML)
]