"""
URL configuration for Edugaya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path , include
from user_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_app/',include('user_app.urls')),
    path("courses_app/", include ('courses_app.urls')),
    path('learning_style/', include('learning_style.urls')),
    path('logout/', views.user_logout, name='logout'),
    path('',views.index,name='index'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
