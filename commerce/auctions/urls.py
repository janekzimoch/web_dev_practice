from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("delete_listing/<str:id>", views.delete_listing, name="delete_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
]
