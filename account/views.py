from django.views import View
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CustomerRegistrationForm, UserForm, CustomerForm


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


def logout_view(request):
    logout(request)
    return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        customer_form = CustomerForm(instance=request.user.customer)
        return render(request, 'account/profile.html', {
            'user_form': user_form,
            'customer_form': customer_form
        })


    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        customer_form = CustomerForm(request.POST, instance=request.user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            messages.success(request, 'Информация обновлена')
            return redirect('home')
        else:
            messages.error(request, 'Обнаружены ошибки')
            return redirect('profile')