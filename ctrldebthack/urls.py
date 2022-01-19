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
from django.urls import path, include
from student import views as sviews
from volunteer import views as vviews

from django.views.generic.base import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('sdashboard/', sviews.match_stud_to_vol),
    path('vdashboard/', vviews.match_vol_to_stud),
    path('stud_chat/<str:name>',sviews.stud_chat),
    path('vol_chat/<str:name>',vviews.vol_chat),
    path('received_messages_by_stud/<str:name>',sviews.messages),
    path('received_messages_by_vol/<str:name>',vviews.messages),
    path('confirm_stud_vol/', vviews.confirm_stud_vol),
    
    path("sinfo/", sviews.sinfo, name='sinfo'),
    path("signin/", sviews.sign_in, name="signin"),
    path("post_signin/", sviews.post_signin),
    path("signup/", sviews.sign_up,name="signup"),
    path("post_signup/", sviews.post_signup),
    path("logout/", sviews.logout),

    path("vinfo/", vviews.vinfo, name='vinfo'),
    path("vsignin/", vviews.vsign_in, name='vsignin'),
    path("vpost_signin/", vviews.vpost_signin),
    path("vsignup/", vviews.vsign_up,name="vsignup"),
    path("vpost_signup/", vviews.vpost_signup),
    path("vlogout/", vviews.vlogout),

    path('', include('admin.urls')),
]

