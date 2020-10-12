"""myrails URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
    # checking if the request url path doesn't trailing with / character
    # if not then redirecting to the same url with / trailer
    re_path(r"^(?P<endpoint>(([\w|/])*\w)(?!/))$", RedirectView.as_view(url="/%(endpoint)s/")),
    re_path(r"", views.page_not_found, name='page_not_found'),

]
