from django.db import models


# 旅游公司
class Agency(models.Model):
    ag_name = models.CharField(max_length=100, verbose_name="公司名")
    ag_tel = models.CharField(max_length=20, verbose_name="公司电话")
    ag_brief = models.TextField(verbose_name="公司简介")

    def __str__(self):
        return self.ag_name

    class Meta:
        db_table = 'agency'
        verbose_name = '旅游公司'
        verbose_name_plural = '旅游公司'
