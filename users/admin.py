from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    # فیلدهایی که در لیست کاربران نمایش داده میشن
    list_display = ('id', 'name', 'username')
    # فیلدی که روی اون میتونی سرچ کنی
    search_fields = ('name', 'username')
    # فیلدهایی که در صفحه ویرایش کاربر نمایش داده میشن
    fields = ('name', 'username', 'password')

# ثبت مدل User با کلاس شخصی سازی شده UserAdmin در پنل ادمین
admin.site.register(User, UserAdmin)