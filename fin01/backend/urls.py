"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def tools(request):
    return render(request, 'home/tools.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/' , include('dashboard.urls') , name='dashboard'),
    path('', lambda request: redirect('dashboard/')),
    path('user/' , include('user.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('tools/' , tools , name = 'tools'),
    path('mvo/' , include("MVO.urls")),
]
