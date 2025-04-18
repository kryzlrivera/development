from django.contrib import admin
from .models import Products, Payment

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('created_at',)  # Corrected tuple with a comma
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'stock', 'product_image')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Assuming product_image or other fields may be ForeignKey
        return queryset.select_related('category')  # Example: Add any ForeignKey field here if needed

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', 'payment_method', 'total_amount', 'created_at')
    list_filter = ('payment_method', 'created_at')
    search_fields = ('name', 'email')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'address', 'payment_method', 'total_amount', 'products')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Assuming payment_method is a ForeignKey, you can optimize it like this:
        return queryset.select_related('payment_method')  # Adjust with your ForeignKey fields
