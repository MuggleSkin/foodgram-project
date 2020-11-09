from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import Social

User = get_user_model()


class UserAdminCustom(UserAdmin):
    search_fields = UserAdmin.search_fields
    search_fields += ('username', 'email',)


admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
admin.site.register(Social)
