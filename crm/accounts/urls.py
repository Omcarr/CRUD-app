from django.urls import path
from django.contrib.auth import views as auth_views 
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
    path('account/',views.accounts_settings,name='account'),

    
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),


]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''

