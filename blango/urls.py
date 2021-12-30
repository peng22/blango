"""blango URL Configuration

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
from django.contrib import admin
from django.urls import path, include
import blango_auth.views
from django_registration.backends.activation.views import RegistrationView
from blango_auth.forms import BlangoRegistrationForm
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from blango_auth.models import User
User.objects.filter(
    is_active=False,
    date_joined__lt=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
).delete()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path("accounts/profile/", blango_auth.views.profile, name="profile"),
    path(
      "accounts/register/",
        RegistrationView.as_view(form_class=BlangoRegistrationForm),
      name="django_registration_register",
      ),
  path("accounts/", include("django_registration.backends.activation.urls")),
  path('accounts/', include('django.contrib.auth.urls')),
  path("accounts/", include("allauth.urls")),

  #here we are using versioning This will allow us 
  #to implement changes to the API without breaking
  # backwards-compatibility with older clients. 
  #While we won't be using it, Django Rest Framework 
  #has support for versioning which allows you to reuse 
  #the same view for different versions and alter the 
  #view's response based on a special version attribute
  # that's available. 
#   path("api/v1/", include("blog.api_urls")),
  path("api/v1/", include("blog.api.urls"))




]
