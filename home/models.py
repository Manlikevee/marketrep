from django.db import models
from django.utils.timezone import now


# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     image = models.URLField()
#     price = models.CharField(max_length=999, blank=True, null=True)
#     category = models.CharField(max_length=999, blank=True, null=True)
# 
#     def __str__(self):
#         return self.name

class market_data(models.Model):
    product_class = models.CharField(max_length=255, blank=True, null=True)
    product_data = models.JSONField(default=list , blank=True, null=True)
    as_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.product_class


class pep_data(models.Model):
    pep_data = models.JSONField(default=list , blank=True, null=True)
    as_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.as_at


class fx_data(models.Model):
    closingrate = models.CharField(max_length=255, blank=True, null=True)
    as_at = models.DateTimeField(default=now)
    def __str__(self):
        return self.as_at
    

class Account_opening_Submission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(default=list , blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_as_at = models.DateTimeField(default=now)
    def __str__(self):
        return self.name