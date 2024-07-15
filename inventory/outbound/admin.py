from django.contrib import admin
from django.http import HttpResponse
import csv
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from .models import Outbound, OutboundItem

class OutboundItemInline(admin.TabularInline):
    model = OutboundItem
    extra = 1


class OutboundAdmin(admin.ModelAdmin):
    list_display = ('transaction_ref', 'total_quantity', 'outbound_date', 'processed_by')
    search_fields = ('transaction_r ef', 'processed_by__username')
    readonly_fields = ('transaction_ref', 'get_items_list')  # Adjusted readonly_fields

    inlines = [OutboundItemInline]  # Include inline form for OutboundItem

    fieldsets = (
        (None, {
            'fields': ('outbound_date', 'processed_by', 'transaction_ref')
        }),
        # ('Unit and Items', {
        #     'fields': ('unit',),
        #     'classes': ('collapse',)  # Optional: Hide by default
        # }),
    )

    def get_queryset(self, request):
        # Override the queryset to annotate with total quantity
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_quantity=Sum('outbounditem__quantity'))
        return queryset

    def total_quantity(self, obj):
        # Display the annotated total quantity
        return obj.total_quantity

    # def unit(self, obj):
    #     return obj.stock.unit if obj.stock else ''

    #     # Override formfield_for_foreignkey to customize the unit field
    #
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'stock':  # Adjust based on your actual foreign key field name
    #         kwargs['queryset'] = Stock.objects.all()  # Replace with your Stock queryset
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    #
    #     # Override save_related to handle saving 'unit' per item
    #
    # def save_related(self, request, form, formsets, change):
    #     super().save_related(request, form    , formsets, change)
    #     obj = form.instance
    #     for formset in formsets:
    #         if isinstance(formset, OutboundItemInline):
    #             instances = formset.save(commit=False)
    #             for instance in instances:
    #                 instance.unit = instance.stock.unit if instance.stock else ''
    #                 instance.save()

    def get_items_list(self, obj):
        # Retrieve and format the list of items associated with this Outbound instance
        items_list = obj.outbounditem_set.all()
        return ', '.join([f'{item.stock.stock_no} ({item.quantity})' for item in items_list])

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="outbound.csv"'

        writer = csv.writer(response)
        writer.writerow(['Transaction Reference', 'Outbound Date', 'Processed By', 'Total Quantity', 'Unit', 'Items'])

        for obj in queryset:
            items_list = obj.outbounditem_set.all()
            writer.writerow(
                [obj.transaction_ref, obj.outbound_date, obj.processed_by, obj.total_quantity, obj.unit, items_list])

        return response

    export_as_csv.short_description = _('Export selected Outbounds as CSV')

    total_quantity.short_description = 'Total Quantity'  # Set the column header
    total_quantity.admin_order_field = 'total_quantity'  # Enable ordering by this column

    # unit.short_description = 'Unit'
    get_items_list.short_description = 'Items'

    # Override save_related to update unit based on first item's stock
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.unit = obj.items.first().unit if obj.items.exists() else ''
        obj.save()

# Register your models with the admin site
admin.site.register(Outbound, OutboundAdmin)
