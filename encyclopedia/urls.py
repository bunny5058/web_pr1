from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("random/", views.random_page, name="random_page"),
    path("edit_page/<str:title>/", views.edit_page, name="edit_page"),
    path("delete_page/<str:title>/", views.delete_page, name="delete_page")
]
