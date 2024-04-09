from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home,name='home'),
    path('product/', views.product,name='product'),
    path('customer/<int:key>/', views.customer,name='customer'),
    path('create_order/<str:key>/', views.CreateOrder,name='create_order'),
    path('create_customer/', views.CreateCustomer,name='create_customer'),

    path('update_order/<str:key>/', views.UpdateOrder,name='update_order'),
    path('update_customer/<str:key>/', views.UpdateCustomer,name='update_customer'),

    path('delete_order/<str:key>/', views.DeleteOrder,name='delete_order'),
    path('delete_customer/<str:key>/', views.deleteCustomer,name='delete_customer'),

    path('login/', views.loginPage, name="login"), 
    path('register/', views.register,name='register'),
	path('logout/', views.logoutUser, name="logout"),
    path('user_page/',views.userProfile,name='user_page'),


]
