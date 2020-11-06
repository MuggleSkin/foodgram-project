from django.urls import path
from . import views

urlpatterns = [
    path("purchase/<int:recipe_id>/", views.purchase, name="purchase"),
    path("purchases/", views.purchase_list, name="purchases"),
    path("shopping_list/", views.get_shopping_list, name="get_shopping_list"),
    path("clear_purchases/", views.clear_purchases, name="clear_purchases"),
]
