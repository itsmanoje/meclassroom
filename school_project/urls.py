# school_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from school_app import views as school_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('school/', include('school_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', school_views.home_redirect, name='home'),  # Add this line
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
