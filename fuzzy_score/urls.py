from django.urls import path

from . import views

app_name = "fuzzy_score"
urlpatterns = [
    path("", views.index, name="index"),
]
