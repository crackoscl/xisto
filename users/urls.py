
# Django
from os import name
from django.urls import path
from .views import Login, Logout, Signup, UpdatePassword,refresh_get,TokenRefresh

app_name = 'users'


urlpatterns = [
    path('get_resfresh_token',refresh_get(),name='get_resfresh_token'),
    path('token_refresh',TokenRefresh.as_view(),name='TokenRefresh'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', Signup.as_view(), name='signup'),
    path('changepassword/', UpdatePassword.as_view(), name='change_pasword'),
]

