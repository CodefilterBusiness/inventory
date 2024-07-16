from django.contrib import admin
from django.http import HttpResponse
import csv
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from .models import Outbound, OutboundItem

class OutboundItemInline(admin.TabularInline):
    model = OutboundItem
    extra = 1
    fields = ('stock', 'stock_name', 'quantity')  # Include 'stock_name' field

    readonly_fields = ('stock_name',)  # Make stock_name readonly

    def stock_name(self, instance):
        return instance.stock.name  # Retrieve and display the name of the stock

    stock_name.short_description = 'Stock Name'


class OutboundAdmin(admin.ModelAdmin):
    list_display = ('transaction_ref', 'total_quantity', 'outbound_date', 'processed_by', 'unit')
    search_fields = ('transaction_ref', 'processed_by__username')
    readonly_fields = ('transaction_ref', 'get_items_list')

    inlines = [OutboundItemInline]

    fieldsets = (
        (None, {
            'fields': ('outbound_date', 'processed_by', 'transaction_ref', 'unit')
        }),
        ('Items', {
            'fields': ('get_items_list',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_quantity=Sum('outbounditem__quantity'))
        return queryset

    def total_quantity(self, obj):
        return obj.total_quantity

    def unit(self, obj):
        return obj.unit.name if obj.unit else ''

    def get_items_list(self, obj):
        items_list = obj.outbounditem_set.all()
        return ', '.join([f'{item.stock.stock_no} ({item.quantity})' for item in items_list])

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="outbound.csv"'

        writer = csv.writer(response)
        writer.writerow(['Transaction Reference', 'Outbound Date', 'Processed By', 'Total Quantity', 'Unit', 'Items'])

        for obj in queryset:
            items_list = obj.outbounditem_set.all()
            items_str = ', '.join([f'{item.stock.stock_no} ({item.quantity})' for item in items_list])
            writer.writerow([obj.transaction_ref, obj.outbound_date, obj.processed_by.username, obj.total_quantity, obj.unit.name if obj.unit else '', items_str])

        return response

    export_as_csv.short_description = _('Export selected Outbounds as CSV')

    total_quantity.short_description = 'Total Quantity'
    total_quantity.admin_order_field = 'total_quantity'
    get_items_list.short_description = 'Items'

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance

        # Deduct stock quantities for all outbound items
        for outbound_item in obj.outbounditem_set.all():
            # Ensure to check if the quantity exceeds available stock
            if outbound_item.quantity > outbound_item.stock.quantity:
                raise ValueError(f"Stock quantity for '{outbound_item.stock.stock_no}' cannot be negative or zero.")

            # Deduct the outbound quantity from stock
            outbound_item.stock.quantity -= outbound_item.quantity
            outbound_item.stock.save()

        # Update the total_quantity field in Outbound model
        obj.total_quantity = obj.outbounditem_set.aggregate(total=Sum('quantity'))['total']
        obj.save()

admin.site.register(Outbound, OutboundAdmin)
