from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jirello/', include('jirello.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT)
    static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)
