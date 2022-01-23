from django.contrib import admin
from django.urls import path
from admin import views

urlpatterns = [
    path("asignin/", views.ad_sign_in, name='ad_signin'),
    path("a_post/", views.admin_post_signin, name='admin_post_signin'),
    path("admin_dash/", views.ad_dashboard, name='ad_dashboard'),
    path("add_admin/", views.add_admin, name='add_admin'),
    path("stud_data/",views.stud_data, name='#stud'),
    path("add_study_material/", views.add_study_material, name="add_study_material"),
    path("get_dash_data/",views.get_dash_data, name="get_dash_data"),
    path("vol_data/",views.vol_data, name='#vol'),
    path("adlogout/", views.ad_logout, name="adlogout")

]