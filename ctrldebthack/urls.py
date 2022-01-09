"""ctrldebthack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from student import views as sviews
from volunteer import views as vviews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_student/', sviews.add_student),
    path('match_stud_to_vol/', sviews.match_stud_to_vol),
    path('add_volunteer/', vviews.add_volunteer),
    path('temp_func/', vviews.temp_func),
    path('frontend_to_backend/', vviews.frontend_to_backend)
]

