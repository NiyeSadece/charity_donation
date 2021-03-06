"""charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

from donation_page import views as dv


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dv.LoadingPageView.as_view(), name='home'),
    path('make-donation/', dv.AddDonationView.as_view(), name='make-donation'),
    path('login/', dv.LoginView.as_view(), name='login'),
    path('register/', dv.RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/', dv.UserView.as_view(), name='user'),
    path('donation-confirmation/', dv.ConfirmationView.as_view(), name='confirmation'),
    path('settings/', dv.change_password, name='settings')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
