from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("timeline/", views.timeline, name="timeline"),
    path("fulltime/", views.fulltime, name="fulltime"),
    path("<int:source_id>/", views.source, name="source"),
    path("<int:source_id>/fetch/", views.fetch_id, name="fetch"),
    path("fetch/", views.fetch_all, name="fetch_all"),
    path("add/", views.add_source, name="add"),
    path("api/item/<int:item_id>/mark/", views.mark_read, name="mark_read"),
]
