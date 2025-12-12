from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست نمایش داده میشن
    list_display = ('id', 'farsi', 'english')
    
    # امکان جستجو
    search_fields = ('farsi', 'english')
    
    # فیلدهای قابل ویرایش در فرم
    fields = ('farsi', 'english')

# ثبت مدل در پنل ادمین
admin.site.register(Category, CategoryAdmin)