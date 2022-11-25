from django.views.generic.list import ListView
from django.shortcuts import render

from .models import Tea


def home(request):
    return render(request, 'catalogue/home.html')


class TeaListView(ListView):
    model = Tea
    context_object_name = 'products'
    template_name = 'catalogue/products.html'

    def get_queryset(self):
        tea_type = self.kwargs.get('tea_type')
        if tea_type:
            return Tea.objects.filter(tea_type=tea_type)
        else:
            return Tea.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tea_type = self.kwargs.get('tea_type')

        if tea_type:
            context['products_title'] = f'{tea_type} Tea'
        
        return context