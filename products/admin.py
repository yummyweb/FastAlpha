from django.contrib import admin
from products.models import Company, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Company)