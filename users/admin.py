from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile
from catalog.models import Item



class ItemInline(admin.StackedInline):
    model = Item
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','qualification')
    search_fields = ['user']
    inlines = [ItemInline]


admin.site.unregister(Group)
admin.site.register(Profile,ProfileAdmin)