from django.contrib import admin
from .models import Ingredient, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "dimension",
    )
    search_fields = ("title",)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients_data.through
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "author",
        "count_favorites",
    )
    filter_horizontal = ("tags",)
    list_filter = ("author",)
    search_fields = ("title",)
    inlines = [RecipeIngredientInline]

    def count_favorites(self, obj):
        return obj.fans.count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
