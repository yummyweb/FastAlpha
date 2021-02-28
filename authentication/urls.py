from django.urls import path 
from authentication.views import Login, Register, UserPage

urlpatterns = [
    path('login/', Login, name="Login"),
    path('register/', Register, name="Register"),
    path('user/<id>/', UserPage, name="User")
]
