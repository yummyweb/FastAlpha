from django.db import models
from authentication.models import User

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to="images/")
    header = models.ImageField(upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant_id = models.CharField(max_length=200, null=True)
    secret_key = models.CharField(max_length=200, null=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    video = models.FileField(upload_to="videos/")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Transaction(models.Model):
    made_by = models.ForeignKey(User, on_delete=models.CASCADE)
    product_invested = models.ForeignKey(Product, on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('FASTALPHAINVESTMENTS%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)