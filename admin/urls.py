from django.contrib import admin
from django.urls import path
from admin import views

urlpatterns = [
    path("asignin/", views.ad_sign_in, name='ad_signin'),
    path("a_post/", views.admin_post_signin, name='admin_post_signin'),
    path("admin_dash/", views.ad_dashboard, name='ad_dashboard'),
    path("add_admin/", views.add_admin, name='add_admin'),
    path("stud_data/",views.stud_data, name='#stud')
]