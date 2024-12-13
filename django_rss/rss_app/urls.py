from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:source_id>/", views.source, name="source"),
    path("<int:source_id>/fetch/", views.fetch, name="fetch"),
    path("add/", views.add_source, name="add"),
]
