from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from tasks import views
from core.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('',home,name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
