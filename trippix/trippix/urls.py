"""
URL configuration for trippix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from home import views


urlpatterns = [
    path(r'home/', views.index, name='home'),
    re_path('admin/', admin.site.urls),
    re_path('login/', views.entry, name='login'),
    re_path('register/', views.register, name='register'),
    re_path('userpage/', views.userpage, name='userpage'),
    re_path('add/', views.add, name='add'),
    path('post/<int:post_id>/', views.post, name='post')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)