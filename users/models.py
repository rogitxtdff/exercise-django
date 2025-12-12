from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام کامل")
    username = models.CharField(max_length=50, unique=True, verbose_name="نام کاربری")
    password = models.CharField(max_length=128, verbose_name="رمز عبور") 
    def __str__(self):
        return f"{self.name} ({self.username})"