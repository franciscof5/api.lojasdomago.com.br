from django.urls import path
from . import views

#from .views import (
#    TodoListApiView,
#)

urlpatterns = [
    path("", views.index, name="index"),
#    path('api', TodoListApiView.as_view()),
]