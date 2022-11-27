from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login

from .forms import CustomerRegistrationForm


class RegistrationView(FormView):
    template_name = 'account/register.html'
    form_class = CustomerRegistrationForm
    success_url = 'home'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('home')
        else:
            return render(request, self.template_name)
