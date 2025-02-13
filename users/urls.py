from django.urls import path
from users.views import assign_role,create_group, admin_dashboard, group_list, activate_user
from users.views import SignUpView, SignInView, SignOutView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/',SignInView.as_view(), name='sign-in'),
    path('sign-out/', SignOutView.as_view(), name='sign-out'),
    path('users/admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/group-list/', group_list, name='group-list'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'), 

]
