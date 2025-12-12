from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'farsi', 'english')
    

    search_fields = ('farsi', 'english')
    

    fields = ('farsi', 'english')


admin.site.register(Category, CategoryAdmin)