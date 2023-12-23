from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("profile/<str:user_name>", views.profile_page, name="profile_page"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("like_post/", views.add_like, name="like_post"),
    path("unlike_post/", views.remove_like, name="unlike_post"),
]
