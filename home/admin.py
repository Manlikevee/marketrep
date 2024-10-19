from django.contrib import admin

from .models import market_data, pep_data,fx_data

#
# # Register your models here.
admin.site.register(market_data)
admin.site.register(fx_data)
