from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
    path("favorites/", views.favorites, name="favorites"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("favorite/<int:recipe_id>/", views.favorite, name="favorite"),
    path("subscribe/<int:author_id>/", views.subscribe, name="subscribe"),
]
