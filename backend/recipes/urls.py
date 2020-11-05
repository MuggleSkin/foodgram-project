from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new_recipe, name="new_recipe"),
    path("favorites/", views.favorites, name="favorites"),
    path("ingredients/", views.ingredients, name="ingredients"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("<username>/", views.profile, name="profile"),
    path("<username>/<int:recipe_id>/", views.recipe_view, name="recipe"),
    path("<username>/<int:recipe_id>/edit/", views.recipe_edit, name="recipe_edit"),
]