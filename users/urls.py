from django.urls import path
from users.views import sign_up, sign_in, sign_out, assign_role,create_group, admin_dashboard, group_list, activate_user

urlpatterns = [
    path('sign-up/', sign_up, name='sign-up'),
    path('sign-in/',sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    # path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
     path('users/admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/group-list/', group_list, name='group-list'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'), 

]
