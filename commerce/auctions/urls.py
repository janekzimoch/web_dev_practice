from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("add_to_watchlist/<str:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<str:id>", views.remove_from_watchlist, name="remove_from_watchlist"),    
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("delete_listing/<str:id>", views.delete_listing, name="delete_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
]
