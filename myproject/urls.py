from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from tasks import views
from core.views import home
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     # import debug_toolbar urlpatterns += [path('__debug__/', include(debug_toolbar.urls)),]
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

