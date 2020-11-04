from django.contrib import admin
from .models import Ingredient, IngredientForRecipe, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "dimension",
    )
    search_fields = ("title",)


class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingredient", "amount", )
    search_fields = ("ingredient",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "author",
    )
    filter_horizontal = ("tags", "ingredients",)
    list_filter = ("author", "title",) 


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
