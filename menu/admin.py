from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'price', 'category', 'description_short')
    

    search_fields = ('name', 'description', 'category__farsi')
    
    list_filter = ('category',)
    
    fields = ('name', 'description', 'price', 'category')
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "-"
    description_short.short_description = "توضیحات"

admin.site.register(MenuItem, MenuItemAdmin)
