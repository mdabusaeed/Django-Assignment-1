from django.urls import path
from users.views import assign_role,create_group, admin_dashboard, group_list, activate_user,ChangePasswordView
from users.views import SignUpView, SignInView, ProfileView, CustomPasswordResetView,CustomPasswordResetConfirmView
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/',SignInView.as_view(), name='sign-in'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('users/admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/group-list/', group_list, name='group-list'),
    path('activate/<int:user_id>/<str:token>/', activate_user, name='activate-user'), 
    path('profile/', ProfileView.as_view(), name='profile'),
    # path('profile/<int:id>/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
