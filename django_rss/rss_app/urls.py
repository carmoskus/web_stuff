from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("source/<int:source_id>/", views.source, name="source"),
    path("source/<int:source_id>/fetch/", views.fetch, name="fetch"),
]
