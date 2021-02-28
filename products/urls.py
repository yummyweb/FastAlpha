from django.urls import path 
from .views import callback, CompanyCreate, CompanyView, Home, MakeInvestment, Products

urlpatterns = [
    path('', Home, name="Home"),
    path('products/', Products, name="Products"),
    path('company/create/', CompanyCreate, name="CreateCompany"),
    path('company/<id>/', CompanyView, name="Company"),
    path('make/investment/<id>/', MakeInvestment, name="MakeInvestment"),
    path('callback/', callback, name="Callback")
]
