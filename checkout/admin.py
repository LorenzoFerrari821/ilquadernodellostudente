from django.contrib import admin
from checkout.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('owner','get_total')
    search_fields = ['owner']


admin.site.register(Cart,CartAdmin)