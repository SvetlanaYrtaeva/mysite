from django.urls import path
from django.contrib.auth.views import LoginView
from .views import MyLogoutView, cookies_read, cookies_set, session_read, session_set

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('cookies/read/', cookies_read, name='cookies_read'),
    path('cookies/set/', cookies_set, name='cookies_set'),
    path('session/read/', session_read, name='session_read'),
    path('session/set/', session_set, name='session_set'),
]