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

def is_admin(user):
    return user.is_superuser or user.groups.filter(name__iexact='admin').exists()

def sign_up(request):
    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            messages.success(request, "Please check your email to activate your account.") 
            return redirect('sign-in')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'registration/login.html', {'form': form})  




@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')


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

# @user_passes_test(is_admin, login_url='no-permission')
# def assign_role(request, user_id):
#     user = User.objects.get(id=user_id)
#     form = AssignRollFrom()

#     if request.method == 'POST':
#         form = AssignRollFrom(request.POST)
#         if form.is_valid():
#             role = form.cleaned_data.get('role')
#             user.groups.clear()
#             user.groups.add(role)
#             messages.success(request, f"{user.username} has been assigned the role of {role}")
#             # return redirect('assign-role', user_id=user_id)
#             return redirect(reverse('assign-role', args=[user_id])) 
        
#     return render(request, 'admin/assign-role.html', {'form': form, 'user': user})


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
