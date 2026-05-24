from django.contrib import admin
from .models import PromoCode

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'value', 'active', 'valid_from', 'valid_to')
    list_filter = ('active', 'discount_type')
    search_fields = ('code',)