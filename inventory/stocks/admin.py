from django.contrib import admin
from .models import Stock

class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_no', 'name', 'unit', 'quantity', 'available', 'last_modified_date')

admin.site.register(Stock, StockAdmin)


