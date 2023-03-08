
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("send_post", views.send_post, name="send_post"),
    path("post/<int:post_id>", views.get_post, name="get_post"),
    path("post/<int:post_id>/like", views.like_post, name="like_post"),
    path("post/<int:post_id>/<int:user_id>/like", views.like_post_get, name="like_post_get"),
]
