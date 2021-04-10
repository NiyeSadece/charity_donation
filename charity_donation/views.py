from django.shortcuts import render
from django.views import View

from .models import Donation


class LoadingPage(View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.all()
        bags = 0
        for donation in donations:
            bags = donation.quantity
        institutions = 0
        for _ in donations.distinct('institution'):
            institutions += 1
        context = {
            'bags': bags,
            'institutions': institutions,
        }
        return render(request, 'index.html', context)


class AddDonation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'form.html')


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')
