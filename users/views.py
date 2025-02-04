from django.shortcuts import render,redirect
from users.forms import UserCreationForm, LoginForm, AssignRollFrom, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.db.models import Prefetch



def sign_up(request):
    form  = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
        messages.success(request, 'Account created successfully, please check your email to activate your account')
        return redirect('login')
    
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')

    return render(request, 'registration/login.html', {'form': form})  


def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    

def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRollFrom()

    if request.method == 'POST':
        form = AssignRollFrom(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request, f"{user.username} has been assigned the role of {role}")
            return redirect('assign-role', user_id=user_id)
        
    return render(request, 'admin/assign-role.html', {'form': form, 'user': user})


def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"{group.name} has been created.")
            return redirect('create-group')
        
    return render(request, 'admin/create-group.html', {'form': form})


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

def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group-list.html', {'groups': groups})