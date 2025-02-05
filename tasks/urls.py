from django.urls import path
from tasks.views import * 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('manager-dashboard/', manager_dashboard, name='manager-dashboard'),
    path('event-list/', event_list, name='event-list'),
    path('update-event/<int:id>/', update_event, name='update_event'),
    path('create-event/', create_event, name='create_event'),
    path('delete-event/<int:id>/', delete_event, name='delete_event'),
    path('create-participant/', create_participant, name='create_participant'),
    path('create-category/', create_category, name='create_category'),
    path('categories/', category_list, name='category_list'),
    path('participant-list/', participant_list, name='participant_list'),
    path('event/', event_page, name='event'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)