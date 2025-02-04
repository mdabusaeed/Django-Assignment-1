from django import forms
from django.contrib.auth.models import User, Permission, Group
import re
from tasks.forms import StyleForMixin
from django.contrib.auth.forms import AuthenticationForm

class UserCreationForm(StyleForMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
         
    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        if len(password1) <8:
            raise forms.ValidationError("Password is too short")
        if not re.search(r'[A-Z]',password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]',password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]',password1):
            raise forms.ValidationError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*()_+]',password1):
            raise forms.ValidationError("Password must contain at least one special character")
        
        return password1
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    
class LoginForm(StyleForMixin, AuthenticationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRollFrom(StyleForMixin,forms.Form):
    role = forms.ModelChoiceField(
        queryset = Group.objects.all(),
        empty_label = "Select a role"
    )

class CreateGroupForm(StyleForMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField( 
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permissions"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
