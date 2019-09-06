from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from .views import LoginView, LogoutView, SignupView
urlpatterns = [
    url('login/', LoginView.as_view(), name='login'),
    url('logout/', LogoutView.as_view(), name='logout'),
    url('signup/', csrf_exempt(SignupView.as_view()), name='signup'),
]
