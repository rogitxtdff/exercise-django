from django.db import models

class Category(models.Model):
    """مدل دسته‌بندی‌ها برای منوی رستوران"""
    farsi = models.CharField(max_length=100, verbose_name="نام فارسی")
    english = models.CharField(max_length=100, verbose_name="نام انگلیسی")
    
    def __str__(self):
        return f"{self.farsi} ({self.english})"
    
    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['farsi'] 