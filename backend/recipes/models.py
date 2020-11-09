from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver

from sorl.thumbnail import delete
from taggit.managers import TaggableManager


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return self.title


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
    ingredients_data = models.ManyToManyField(
        Ingredient,
        related_name="recipes",
        through="RecipeIngredient",
    )
    tags = TaggableManager()

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    data = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients"
    )
    amount = models.PositiveIntegerField()

    class Meta:
        unique_together = ("data", "recipe")

    def __str__(self):
        return (
            f"{self.data.title} "
            f"({self.data.dimension}) - {self.amount}"
        )


@receiver(models.signals.post_delete, sender=Recipe)
def auto_delete_image_on_delete(**kwargs):
    """
    Deletes image from filesystem
    when corresponding `Recipe` object is deleted.
    """
    instance = kwargs["instance"]
    if instance.image:
        delete(instance.image)


@receiver(models.signals.pre_save, sender=Recipe)
def auto_delete_image_on_change(**kwargs):
    """
    Deletes old image from filesystem
    when corresponding `Recipe` object is updated
    with new image.
    """
    instance = kwargs["instance"]
    try:
        old_image = Recipe.objects.get(pk=instance.pk).image
        new_image = instance.image
    except Recipe.DoesNotExist:
        return

    if old_image and (not old_image == new_image):
        delete(old_image)
