from django.urls import path
from .views import *
urlpatterns = [
    path('',home_view,name='home-view'),
    #path('about/',about,name='about'),
    path('donor/register/',donorsignup,name='donor-signup'),
    path('login/',login_view,name='login-view'),
    path('donor/home/',donorhome,name='donor-home'),
    path('donor/profile/',donorprofile,name='donor-profile'),
    path('donor/home/<int:pk>/',donororg,name='donor-org'),
    path('organization/register/',orgsignup,name='org-signup'),
    path('organization/profile/',orgprofile,name='org-profile'),
    path('organization/home/',orghome,name='org-home'),
    path('organization/approve/',orgapproval,name='org-approve'),
    path('admins/register/',adminsignup),
    path('admins/home/',adminorglist,name='admin-dashboard'),
    path('admins/home/<int:pk>/',adminorg,name='admin-org'),
    # path('organization/register/upload_files/',org_uploadfiles),
    # path('organization/login/',org_login),
    
    path('logoutUser/',logoutUser,name='logout-view')
    # Add other URLs as needed
]
