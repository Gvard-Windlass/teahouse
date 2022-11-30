from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    birthday = forms.DateField(required=True)

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