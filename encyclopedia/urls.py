from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("results", views.results, name="results"),
    path("create", views.create, name="create"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("random_entry", views.random_entry, name="random_entry")
    
    
]
