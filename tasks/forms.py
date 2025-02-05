from django import forms
from tasks.models import Event, Category
from django.contrib.auth.models import User


class StyleForMixin:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widged()
        
    default_classes = "border-2 border-blue-300 w-full px-4 py-2 rounded-lg shadow-md bg-gradient-to-r from-blue-100 to-blue-200 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500 transition duration-300"
    def apply_style_widged(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': "border-2 border-green-300 px-4 py-2 rounded-lg shadow-md bg-gradient-to-r from-green-100 to-green-200 focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-500 transition duration-300"
                })

            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': "space-y-2 border-2 border-pink-300 rounded-lg shadow-md bg-pink-100 focus:outline-none focus:ring-2 focus:ring-pink-500"
                })
            else:

                field.widget.attrs.update({
                    'class': self.default_classes
                })

class EventForm(StyleForMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'image', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'})
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widged()

class ParticipantForm(StyleForMixin,forms.ModelForm):  
    class Meta:
        model = User  
        fields = ['email', 'first_name', 'last_name'] 
        widgets = {
            'events': forms.CheckboxSelectMultiple(),  
        }

    events = forms.ModelMultipleChoiceField(queryset=Event.objects.all(), required=False)


class CategoryForm(StyleForMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.apply_style_widged() 

