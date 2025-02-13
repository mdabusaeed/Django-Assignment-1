from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from users.forms import UserCreationForm, LoginForm, AssignRollFrom, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from users.forms import LoginForm, AssignRollFrom, CreateGroupForm
from django.contrib.auth.tokens import default_token_generator 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.urls import reverse
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
 

def is_admin(user):
    return user.is_superuser or user.groups.filter(name__iexact='admin').exists()

class SignUpView(View):
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, "Please check your email to activate your account.") 
            return redirect('sign-in')
        return render(request, self.template_name, {'form': form})


class SignInView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True 

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else reverse_lazy('home') 

    
class SignOutView(LogoutView):
    next_page = reverse_lazy('sign-in')


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid Token")
        
    except User.DoesNotExist:
        return HttpResponse ("User Not Found")


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user = get_object_or_404(User, id=user_id)  # ✅ Prevents errors if user doesn't exist
    form = AssignRollFrom()

    if request.method == 'POST':
        form = AssignRollFrom(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # ✅ Removes old roles
            user.groups.add(role)  # ✅ Assigns new role
            messages.success(request, f"{user.username} has been assigned the role of {role}")
            return redirect(reverse('assign-role', args=[user_id]))  # ✅ Uses reverse()

    return render(request, 'admin/assign-role.html', {'form': form, 'user': user})



@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"{group.name} has been created.")
            return redirect('create-group')
        
    return render(request, 'admin/create-group.html', {'form': form})


@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name 
        else: 
            user.group_name = 'No Groupe Assigned'
        

    return render(request, 'admin/admin-dashboard.html', {'users': users})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group-list.html', {'groups': groups})

from django.shortcuts import render

def home(request):
    print(f"DEBUG: Current logged-in user: {request.user}")  # Should print "Babor"
    return render(request, "home.html")


