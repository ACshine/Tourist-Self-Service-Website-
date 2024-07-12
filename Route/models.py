from django.db import models
from Agency.models import Agency


# 线路
class Route(models.Model):
    rt_name = models.CharField(max_length=100, verbose_name="线路名")
    ag_id = models.ForeignKey(Agency, on_delete=models.CASCADE, verbose_name="所属公司")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="价格")
    rt_brief = models.TextField(verbose_name="线路简介")

    def __str__(self):
        return self.rt_name

    class Meta:
        db_table = 'route'
        verbose_name = '旅游线路'
        verbose_name_plural = '旅游线路'
