from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from recipes.models import Recipe


class Purchase(models.Model):
    session = models.OneToOneField(
        Session, on_delete=models.CASCADE,
        related_name="purchase", verbose_name="сессия"
    )
    recipes = models.ManyToManyField(Recipe, verbose_name="рецепты")


@receiver(post_save, sender=Session)
def create_purchase(sender, instance, created, **kwargs):
    if created:
        Purchase.objects.get_or_create(session=instance)
