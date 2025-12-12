from django.db import models
from categories.models import Category  # ایمپورت مدل دسته‌بندی

class MenuItem(models.Model):
    """مدل آیتم‌های منوی رستوران"""
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='menu_items',
        verbose_name="دسته‌بندی"
    )
    
    def __str__(self):
        return f"{self.name} - {self.price} تومان"
    
    class Meta:
        verbose_name = "آیتم منو"
        verbose_name_plural = "آیتم‌های منو"
        ordering = ['category', 'name']