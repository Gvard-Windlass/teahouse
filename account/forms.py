from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from .models import Customer


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    birthday = forms.DateField(required=True, label=_('birthday'), widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birthday', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(CustomerRegistrationForm, self).save(commit=True)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.customer.birthday = self.cleaned_data['birthday']
        user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('birthday', 'avatar')
        widgets = {
            'birthday': forms.TextInput(attrs={'type': 'date'})
        }