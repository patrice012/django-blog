from django.urls import path

from django.urls import path

from authapp import views


app_name = "authapp"
urlpatterns = [
    path('signup/', views.signup, name= 'account_signup'),
    path("login/", views.loginUser, name="account_login"),
    path("logout/", views.logoutUser, name="account_logout"),
   	path('changepassword/', views.PasswordChange, name='change_password'),
   	path('changepassword/done', views.PasswordChangeDone, name='change_password_done'),

]