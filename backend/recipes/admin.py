from django.contrib import admin
from .models import Ingredient, RecipeIngredient, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "dimension",
    )
    search_fields = ("title",)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "data", "amount", )
    search_fields = ("data",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "author",
        "count_favorites",
    )
    filter_horizontal = ("tags", "ingredients_data",)
    list_filter = ("author", "title",)

    def count_favorites(self, obj):
        return obj.fans.count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
