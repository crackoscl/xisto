
# Django
from os import name
from django.urls import path
from .views import Login, Logout, Signup, UpdatePassword,refresh_get,TokenRefresh

app_name = 'users'


urlpatterns = [
    path('get_resfresh_token',refresh_get,name='get_resfresh_token'), #obtiene el token de refresh
    path('token_refresh',TokenRefresh.as_view(),name='TokenRefresh'), # obtiene un nuevo access
    path('login/', Login.as_view(), name='login'), #genera token de acces y refresh
    path('logout/', Logout.as_view(), name='logout'), # remueve la cookie 
    path('signup/', Signup.as_view(), name='signup'), # crea un nuevo usuario y te envia un link token al correo
    path('changepassword/', UpdatePassword.as_view(), name='change_pasword'), # cambia la password
]

