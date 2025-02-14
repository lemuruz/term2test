from django.urls import path
from . import views

app_name = "mypoll"

urlpatterns = [
    path("", views.index, name="index"),
    path("vote/", views.vote, name="vote"),
    path("votepage/<int:poll_id>/", views.vote_page, name="votepage"),
    path('result/<int:poll_id>/', views.result, name="result")
]