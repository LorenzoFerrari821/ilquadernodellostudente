from django.contrib import admin
from .models import Item,HaveItem,ReviewsObject

admin.site.site_header="Pannello di amministrazione di Ilquadernodellostudente"
admin.site.site_title = "Ilquadernodellostudente"


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','vendor','school_level','subject','vote','price')
    list_filter = ('school_level','subject')
    search_fields = [('name','vendor','vote','price')]

admin.site.register(Item,ItemAdmin)
admin.site.register(HaveItem)
admin.site.register(ReviewsObject)




