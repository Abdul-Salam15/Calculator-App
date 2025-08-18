from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name = "index" ),
    path("index/", views.index, name = "index" ),
    path("solve/", views.solve, name = "solve"),
    path("history/", views.history, name = "history"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", views.register, name="register"),  # custom view you’ll make

]
