from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from users.forms import RegistrationForm, LoginForm
from .models import Donation, Institution, Category


class LoadingPageView(View):
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
        return render(request, 'donation_page/index.html', context)


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.all(),
            'institutions': Institution.objects.all(),
        }
        return render(request, 'donation_page/form.html', context)

    def post(self, request, *args, **kwargs):
        institution = request.POST.get('organization')
        categories = Category.objects.filter(pk=request.POST.get('categories'))
        post_data = {
            'quantity': request.POST.get('bags'),
            'institution': Institution.objects.get(pk=institution),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('postcode'),
            'phone_number': request.POST.get('phone'),
            'pick_up_date': request.POST.get('data'),
            'pick_up_time': request.POST.get('time'),
            'pick_up_comment': request.POST.get('more_info'),
            'user': request.user
        }
        donation = Donation.objects.create(**post_data)
        for category in categories:
            donation.categories.add(category)
        return redirect('confirmation')


class ConfirmationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'donation_page/form-confirmation.html')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'donation_page/login.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
                            password=cd['password'])

        if user:
            login(self.request, user)
            return redirect('home')
        return redirect('register')

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return redirect('register')


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'donation_page/register.html'

    def form_valid(self, form):
        user = form.save()
        if user:
            return redirect('login')
        return super().form_valid(form)


class UserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        donations = Donation.objects.filter(user=request.user.id)
        return render(request, 'donation_page/user.html', {'donations': donations})


# class SettingsView(LoginRequiredMixin, FormView):
#     form_class = PasswordChangeForm
#     template_name = 'donation_page/settings.html'
#
#     def form_valid(self, form):
#         user = form.save()
#         update_session_auth_hash(self.request, user)
#         return render()

@method_decorator(csrf_exempt, name='dispatch')
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('user')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'donation_page/settings.html', {
        'form': form
    })
