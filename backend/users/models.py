from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from recipes.models import Recipe

User = get_user_model()


class Social(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    following = models.ManyToManyField(
        User,
        related_name="followers",
        verbose_name="подписки"
    )
    favorites = models.ManyToManyField(
        Recipe,
        related_name="fans",
        verbose_name="избранное"
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Social.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.social.save()
