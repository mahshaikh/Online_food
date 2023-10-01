from django.urls import path
from .import views

urlpatterns = [
    path('registerUser/',views.registerUser,name='registerUser'),
    path('registerVendor/',views.registervendor,name='registerVendor'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('my_Account/',views.my_Account,name='my_Account'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),
]