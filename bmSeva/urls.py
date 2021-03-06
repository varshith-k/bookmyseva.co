"""bmSeva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from user import views as user_view
from django.contrib.auth import views as auth
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('login/', user_view.Login, name ='login'),
    path('profile/',user_view.profile_info,name='profile'),
    path('logout/', auth.LogoutView.as_view(template_name ='index.html'), name ='logout'),
    path('services/',user_view.prof_list,name='profss'),
    path('edit/',user_view.edit_profile,name='editpro'),
    path('register/', user_view.register, name ='register'),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
