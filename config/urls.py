"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import TemplateView
from django.shortcuts import render

# Update the vue_app view to handle all cases
def vue_app(request, path=''):  # Make path optional with default value
    """Serve the Vue app for all non-API routes"""
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('smartplan.urls')),
    # Handle the root path
    path('', vue_app, name='vue-app'),
    # Handle all other paths
    path('<str:path>', vue_app, name='vue-app-with-path'),
    # Handle nested paths
    path('<path:path>/', vue_app, name='vue-app-with-nested-path'),
]
