from django.contrib import admin
from django.urls import path, include
from mainapp.views import home, account
from django.conf.urls import handler403, handler404

urlpatterns = [
    path("", include("mainapp.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", account.AccountSignUpView.as_view(), name="signup"),
    path("accounts/login", home.LoginView.as_view(), name="login"),
    path("admin/", admin.site.urls),
]

handler403 = home.custom_403_view
handler404 = home.custom_404_view
 