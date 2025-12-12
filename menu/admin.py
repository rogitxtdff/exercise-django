from django.contrib import admin
from .models import MenuItem

class MenuItemAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست نمایش داده میشن
    list_display = ('id', 'name', 'price', 'category', 'description_short')
    
    # امکان جستجو
    search_fields = ('name', 'description', 'category__farsi')
    
    # فیلتر بر اساس دسته‌بندی
    list_filter = ('category',)
    
    # فیلدهای قابل ویرایش در فرم
    fields = ('name', 'description', 'price', 'category')
    
    # تابع برای نمایش توضیحات کوتاه
    def description_short(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "-"
    description_short.short_description = "توضیحات"

# ثبت مدل در پنل ادمین
admin.site.register(MenuItem, MenuItemAdmin)
