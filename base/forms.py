from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Appointment
class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','password_confirm']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already in use')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match')
        else:
            return cleaned_data
        

class AppointmentForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'form-control','type':'datetime-local'}))

    class Meta:
        model = Appointment
        fields = ['title','description','start_time','end_time']