from django.urls import path
from . import views

app_name = "mypoll"

urlpatterns = [
    path("", views.index, name="index"),

]