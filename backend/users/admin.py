from django.contrib import admin
from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author",)


admin.site.register(Follow, FollowAdmin)
