from django.db import models
from django.contrib.auth.models import User


class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    user_type = models.CharField(max_length=20, choices=[('regular', '普通用户'), ('vip', 'VIP用户'),('admin','网站管理员'),('agent','旅行社人员')], default='regular', verbose_name="用户类型")
    is_sign_in = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '旅客'
        verbose_name_plural = '旅客'

class FrequentTraveler(models.Model):
    user = models.ForeignKey(Tourist, related_name='frequent_travelers', on_delete=models.CASCADE, verbose_name="用户")
    name = models.CharField(max_length=100, verbose_name="姓名")
    phone_number = models.CharField(max_length=20, verbose_name="电话")
    ID_TYPE_CHOICES = [
        ('身份证', '身份证'),
        ('护照', '护照'),
        ('驾照', '驾照'),
        ('其他', '其他'),
    ]
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES, verbose_name="证件类型")
    id_number = models.CharField(max_length=50, verbose_name="证件号码")
    nationality = models.CharField(max_length=100, verbose_name="国籍")
    GENDER_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="性别")

    def __str__(self):
        return f'{self.name} ({self.user.username})'

    class Meta:
        db_table = 'frequent_traveler'
        verbose_name = '常用旅客'
        verbose_name_plural = '常用旅客'


