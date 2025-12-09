# club/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Resource, Unit, Event

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title','unit','resource_type','file','description']

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            max_mb = 20
            if f.size > max_mb * 1024 * 1024:
                raise forms.ValidationError(f"Max file size is {max_mb}MB")
        return f

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['year','title','code']

class EventForm(forms.ModelForm):
    start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    end = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
    class Meta:
        model = Event
        fields = ['title','description','location','start','end','poster']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Event description'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event location'
            }),
            'start': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'poster': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }