from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import Donation, Institution


# class LoadingPage(ListView):
#     model = Institution
#     context_object_name = 'institutions'
#     template_name = 'index.html'
#     paginate_by = 5
#     bags = 0
#     donations = Donation.objects.all()
#
#     @staticmethod
#     def get_foundations():
#         return Institution.objects.filter(type=1)
#
#     @staticmethod
#     def get_ngos():
#         return Institution.objects.filter(type=2)
#
#     @staticmethod
#     def get_local():
#         return Institution.objects.filter(type=3)
#
#     @staticmethod
#     def get_bags_count():
#         donations = Donation.objects.all()
#         for donation in donations:
#             bags = donation.quantity
#         return bags
#
#     @staticmethod
#     def get_institutions_count():
#         institutions_count = 0
#         donations = Donation.objects.all()
#         for _ in donations.distinct('institution'):
#             institutions_count += 1
#         return institutions_count


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
        paginator1 = Paginator(institutions_fun_list, 5)
        paginator2 = Paginator(institutions_ngo_list, 5)
        paginator3 = Paginator(institutions_local_list, 5)
        page = request.GET.get('page')
        institutions_fun = paginator1.get_page(page)
        institutions_ngo = paginator2.get_page(page)
        institutions_local = paginator3.get_page(page)

        context = {
            'bags': bags,
            'institutions_count': institutions_count,
            'foundations': institutions_fun,
            'ngos': institutions_ngo,
            'local_donations': institutions_local,
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
