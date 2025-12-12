from django.db import models

class User(models.Model):
    # id به طور خودکار توسط جنگو ساخته میشه (AutoField)
    name = models.CharField(max_length=100, verbose_name="نام کامل")
    username = models.CharField(max_length=50, unique=True, verbose_name="نام کاربری")
    password = models.CharField(max_length=128, verbose_name="رمز عبور") # طول 128 برای الگوریتم های هش مناسب است

    def __str__(self):
        return f"{self.name} ({self.username})"