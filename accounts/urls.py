from django.urls import re_path
from .views import UserRegister, UserLogin, UserAll


urlpatterns = [
    re_path(r'^user/all/$', UserAll.as_view(),name="all_user"),
    re_path(r'^user/register/$', UserRegister.as_view(),name="register"),
    re_path(r'^user/login/$', UserLogin.as_view(),name="login"),
]