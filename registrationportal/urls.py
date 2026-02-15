from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views as reg_views
from django.views.generic import RedirectView
urlpatterns = [
    path('' , reg_views.home,name="home"),
    path('rulebook/', reg_views.rulebook, name="rulebook"),
    path('contact/', reg_views.contact, name="contact"),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('competitions/', include('competitions.urls')),
    path('offlineportal/', include('apps.offlinePortal.urls')),
    path('accounts/', include('allauth.urls')),
    path('sponsors_workshop/', reg_views.sponsor, name="sponsors_workshop"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
