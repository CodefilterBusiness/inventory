from django.contrib import admin
from .models import Stock

class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_no', 'name', 'unit', 'quantity', 'available', 'last_modified_date')
    search_fields = ('stock_no', 'name')  # Fields to search in the admin interface

admin.site.register(Stock, StockAdmin)


