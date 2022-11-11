from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.render_page, name="page"),
    path("search", views.search, name="search"),
    path("create_new_page", views.create_new_page, name="create_new_page"),
]
