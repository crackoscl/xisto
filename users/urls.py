
# Django
from os import name
from django.urls import path
from .views import Login, Logout, Signup, UpdatePassword

app_name = 'users'


urlpatterns = [
    path('logout/', Logout.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('changepassword/', UpdatePassword.as_view(), name='change_pasword'),
]

