from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return self.ingredient.title + ' ' + \
            str(self.amount) + self.ingredient.dimension


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        "date published", auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    ingredients = models.ManyToManyField(IngredientForRecipe, related_name="recipes")
    tags = TaggableManager()

    def __str__(self):
        return self.title

