from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
    path("subscribe/<int:author_id>/", views.subscribe, name="subscribe"),
    path("unsubscribe/<int:author_id>/",
        views.unsubscribe,
        name="unsubscribe"
    ),
]
