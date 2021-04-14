from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login

from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Donation, Institution


class LoadingPage(View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        bags = 0
        institutions_count = 0

        for donation in donations:
            bags += donation.quantity

        for _ in donations.distinct('institution'):
            institutions_count += 1

        institutions_fun_list = Institution.objects.filter(type=1)
        institutions_ngo_list = Institution.objects.filter(type=2)
        institutions_local_list = Institution.objects.filter(type=3)
        # paginator1 = Paginator(institutions_fun_list, 5)
        # paginator2 = Paginator(institutions_ngo_list, 5)
        # paginator3 = Paginator(institutions_local_list, 5)
        # page = request.GET.get('page')
        # institutions_fun = paginator1.get_page(page)
        # institutions_ngo = paginator2.get_page(page)
        # institutions_local = paginator3.get_page(page)

        context = {
            'bags': bags,
            'institutions_count': institutions_count,
            'foundations': institutions_fun_list,
            'ngos': institutions_ngo_list,
            'local_donations': institutions_local_list,
        }
        return render(request, 'index.html', context)


class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'form.html')


class Login(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        info = form.cleaned_data
        user = authenticate(username=info['username'],
                            password=info['password'])

        if user:
            login(self.request, user)
            return redirect('home')
        return redirect('register')


class Register(FormView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        if user:
            return redirect('login')
        return super().form_valid(form)
