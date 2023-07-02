from . import views
from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('verify_email', views.VerifyEmailAPIView.as_view(), name="verify_email"),
    path('email_verify_code_check', views.VerificationCodeCheckAPIView.as_view(), name="code_check"),
    path('forgot_password', views.ForgotPasswordAPIView.as_view(), name="forgot_password"),
    path('change_password', views.SetNewPasswordAPIView.as_view(), name="change_password"),
    path('user_detail', views.UserDetailAPIView.as_view(), name="user_detail"),
    path('user_update', views.UserUpdateAPIView.as_view(), name="user_update"),

]
