from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return (f"{self.ingredient.title} "
        f"({self.ingredient.dimension}) - {self.amount}")


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
    image = models.ImageField(upload_to="recipes/", null=True)
    ingredients = models.ManyToManyField(
        RecipeIngredient,
        related_name="recipes",
    )
    tags = TaggableManager()

    def __str__(self):
        return self.title

