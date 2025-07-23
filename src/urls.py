from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView

urlpatterns = [
  path('', include('yfcases.urls')),
  path('admin/', admin.site.urls),
  path('users/', include('users.urls')),
  path('users/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
