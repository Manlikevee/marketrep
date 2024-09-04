from django.db import models
from django.utils.timezone import now


# Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     image = models.URLField()
#     price = models.CharField(max_length=999, blank=True, null=True)
#
#     def __str__(self):
#         return self.name





class market_data(models.Model):
    product_class = models.CharField(max_length=255, blank=True, null=True)
    product_data = models.JSONField(default=list , blank=True, null=True)
    as_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.product_class