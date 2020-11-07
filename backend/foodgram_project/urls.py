from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


handler404 = "users.views.page_not_found"
handler500 = "users.views.server_error" 


urlpatterns = [
    path("auth/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path("", include("purchases.urls")),
    path("", include("users.urls")),
    path("", include("recipes.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
